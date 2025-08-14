from pathlib import Path
import duckdb
from loguru import logger
from nicegui import ui
from uuid import uuid4


def write_note(output_dir: Path, note_title: str, note_text: str):

    note_uuid = uuid4()
    logger.debug(note_uuid)
    logger.debug(type(note_uuid))

    output_path = output_dir / f"{str(note_title)}-{note_uuid}.txt" 

    logger.info(f"Writing file: {str(output_path)}")
    with output_path.open("w", encoding="utf8"):
        output_path.write_text(str(note_text))

    ui.notify("Note saved!")

    return note_uuid
