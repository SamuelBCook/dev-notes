from pathlib import Path
import duckdb
from loguru import logger
from nicegui import ui
import json
from db_utils import insert_note
from uuid import uuid4
import re
from uuid import UUID
from typing import Optional


def write_note_handler(
    title_input: ui.textarea,
    text_input: ui.textarea,
    output_dir: Path,
    db_path: Path,
    extension: str,
    note_uuid: UUID
):
        
    note_path = output_dir / f"{str(title_input.value)}-{str(note_uuid)}{extension}"

    note_tags = check_for_tags(text=text_input.value)

    write_note(note_path=note_path, note_text=text_input.value)

    insert_note(
        note_uuid=note_uuid,
        db_path=db_path,
        note_title=title_input.value,
        note_path=note_path,
        note_tags=note_tags
    )

def write_note(note_path: Path, note_text: str):

    logger.info(f"Writing file: {str(note_path)}")
    with note_path.open("w", encoding="utf8"):
        note_path.write_text(str(note_text))

    ui.notify("Note saved!")


def read_settings(settings_path: Path):

    if not settings_path.exists():
        logger.error(f"Settings file does not exist: {settings_path}")
        raise FileExistsError

    with settings_path.open("r", encoding="utf-8") as f:
        settings = json.load(f)

    return settings


def overwrite_settings(settings_path: Path, settings: dict):

    if not settings_path.exists():
        logger.error(f"Settings file does not exist: {settings_path}")
        raise FileExistsError

    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

    logger.info('Updated settings')


def check_for_tags(text:str):

    if text is None:
        return []

    # Double \\ as \ is escaped in regex strings
    matches = re.findall(r'\\@(\S+)', text)

    if matches:
        logger.debug(f'Tags detected!: {matches}')
        return matches
    
    return []