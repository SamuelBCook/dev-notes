from pathlib import Path
from db_utils import select_all_notes
from nicegui import ui


def find_main(db_path:Path):
    notes_table = create_notes_table(db_path=db_path)


def create_notes_table(db_path: Path):

    notes_df = select_all_notes(db_path=db_path)
    table = ui.table.from_pandas(
        notes_df,
        column_defaults={
            "align": "left",
            "headerClasses": "uppercase text-primary",
            "sortable": True,
        },
    ).classes("max-h-40")

    return table