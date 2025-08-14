import duckdb
from pathlib import Path
from loguru import logger
from typing import Optional
import pandas as pd
from uuid import uuid4

def select_all_notes(db_path: Path):

    with duckdb.connect(str(db_path)) as con:

        notes_df = con.execute(
            """
            SELECT title, note_path, datetime FROM notes WHERE is_deleted = FALSE;
            """
        ).df()

        notes_df['datetime'] = pd.to_datetime(notes_df['datetime'])
        notes_df.rename(columns={'title': 'Title', 'datetime': 'Created', 'note_path':'File path'}, inplace=True)

        return notes_df


def insert_note(db_path: Path, note_title: str, note_path: Path, note_uuid:uuid4, note_tags:Optional[list[str]] = None):

    with duckdb.connect(str(db_path)) as con:

        try:

            con.execute("BEGIN TRANSACTION;")

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
                {'note_id': note_uuid, "note_title": note_title, "note_path": str(note_path)},
            )

            if note_tags:
                for tag in note_tags:
                    con.execute(
                        f"""
                        INSERT INTO tags (tag)
                        VALUES ($tag);
                        """,
                        {"tag": tag},
                    )

                    con.execute(
                        f"""
                        INSERT INTO note_tags (note_id, tag_id)
                        VALUES (
                            (
                                SELECT id FROM notes WHERE title = note_title
                            ),
                            (
                                SELECT id FROM tags WHERE name = tag
                            )
                        );
                        """
                    )

            con.execute("COMMIT;")

        except Exception as e:

            logger.error(f"Error inserting note: {e}")
            con.execute("ROLLBACK;")
            raise


def create_tables(db_path: Path):

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
                    id UUID PRIMARY KEY DEFAULT uuid(),
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
                    tag TEXT NOT NULL,
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


