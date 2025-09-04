import duckdb
from duckdb import ConstraintException

from pathlib import Path
from loguru import logger
from typing import Optional
import pandas as pd
from uuid import UUID

from decorators import careful_con
from duckdb import DuckDBPyConnection

@careful_con
def select_all_tags(con: DuckDBPyConnection):
    
    tags_df = con.execute("""
                SELECT 
                n.id AS note_id,
                n.title,
                t.id AS tag_id,
                t.tag
                FROM notes n
                JOIN note_tags nt ON n.id = nt.note_id
                JOIN tags t ON nt.tag_id = t.id
                WHERE n.is_deleted = FALSE 
                AND t.is_deleted = FALSE;
                """).fetch_df()
    
    return tags_df

    
@careful_con
def select_all_notes(con: DuckDBPyConnection):

    notes_df = con.execute(
        """
        SELECT id as note_id, title, note_path, datetime FROM notes WHERE is_deleted = FALSE;
        """
    ).df()

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
                

@careful_con
def init_db_config(con: DuckDBPyConnection):

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

    logger.debug("Database created successfully!")

      
