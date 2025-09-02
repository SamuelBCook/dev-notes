import duckdb
from duckdb import ConstraintException

from pathlib import Path
from loguru import logger
from typing import Optional
import pandas as pd
from uuid import UUID

from decorators import careful_con
from duckdb import DuckDBPyConnection


def select_all_notes(db_path: Path):

    with duckdb.connect(str(db_path)) as con:

        notes_df = con.execute(
            """
            SELECT title, note_path, datetime FROM notes WHERE is_deleted = FALSE;
            """
        ).df()

        notes_df["datetime"] = pd.to_datetime(notes_df["datetime"])
        notes_df.rename(
            columns={"title": "Title", "datetime": "Created", "note_path": "File path"},
            inplace=True,
        )

        return notes_df

def insert_tags(
        con: DuckDBPyConnection,
        note_tags: list[str],
        note_uuid: UUID

):
    
    logger.debug(f'Inserting tags for note: {note_uuid}')
    
    for tag in set(note_tags):

        # Check if tag exists 
        tag_exists = con.execute(
            "SELECT EXISTS(SELECT 1 FROM tags WHERE tag = $tag) as tag_exists;",
            {"tag": tag}
        ).fetchone()[0]

        if tag_exists:
            logger.debug(f"Tag '{tag}' already exists, skipping insertion.")

        else:
            # Insert tag into tag table
            con.execute(
                f"""
                INSERT INTO tags (tag)
                VALUES ($tag);
                """,
                {"tag": tag},
            )
            logger.debug(f'Tag inserted: {tag}')

        # Check if link already exists
        link_exists = con.execute(
            "SELECT EXISTS(SELECT 1 FROM note_tags WHERE note_id = $note_id AND tag_id = (SELECT id FROM tags WHERE tag = $tag)) as link_exists;",
            {"note_id": note_uuid, "tag": tag}
        ).fetchone()[0]

        if link_exists:
            logger.debug(f"Link between note '{note_uuid}' and tag '{tag}' already exists, skipping insertion.")
            continue

        # Update link table
        con.execute(
            f"""
            INSERT INTO note_tags (note_id, tag_id)
            VALUES (
                (
                    SELECT id FROM notes WHERE id = $note_id
                ),
                (
                    SELECT id FROM tags WHERE tag = $tag
                )
            );
            """,
            {"note_id": note_uuid, "tag": tag}
        )
        logger.debug(f'Inserted tag {tag} for note {note_uuid}')


@careful_con
def insert_note(
    con: DuckDBPyConnection,
    note_title: str,
    note_path: Path,
    note_uuid: UUID, 
    note_tags: Optional[list[str]] = None,
):
    
    logger.debug(f'Inserting note: {note_uuid}')


    # Check if note already exists
    exists = con.execute(
    """
    SELECT EXISTS(
    SELECT 1 FROM notes WHERE id = $note_uuid
    ) as id_exits;
    """,
    {"note_uuid": note_uuid},
    ).fetchone()[0]

    logger.debug(f'Note already exists: {exists}')

    if not exists:

        con.execute(
            f"""
            INSERT INTO notes (
                id,
                title,
                note_path
            )
            VALUES (
                $note_id,
                $note_title,
                $note_path
            );
            """,
            {"note_id": note_uuid, "note_title": note_title, "note_path": str(note_path)},
        )

    if note_tags:
        insert_tags(con=con, note_tags=note_tags, note_uuid=note_uuid)
                


def init_db_config(db_path: Path):

    if db_path.exists():
        logger.debug(f"Database already exists at: {str(db_path)}")
        return

    else:

        with duckdb.connect(str(db_path)) as con:

            try:

                con.execute("BEGIN TRANSACTION;")

                con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                    id UUID PRIMARY KEY,
                    title TEXT NOT NULL,
                    note_path TEXT NOT NULL,
                    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_deleted BOOL DEFAULT FALSE
                    );
                    """
                )

                con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS tags (
                    id UUID PRIMARY KEY DEFAULT uuid(),
                    tag TEXT NOT NULL UNIQUE,
                    is_deleted BOOL DEFAULT FALSE
                    );
                    """
                )

                con.execute(
                    """
                    CREATE TABLE IF NOT EXISTS note_tags (
                    note_id UUID REFERENCES notes(id),
                    tag_id UUID REFERENCES tags(id),
                    PRIMARY KEY (note_id, tag_id)
                    );
                    """
                )

                con.execute("COMMIT;")
                logger.debug("Database created successfully!")

            except Exception as e:

                logger.error(f"Error creating tables: {e}")
                con.execute("ROLLBACK;")
                raise
