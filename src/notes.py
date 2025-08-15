from nicegui import ui
from datetime import datetime
from backend import write_note_handler
from pathlib import Path

def notes_main(output_dir:Path, db_path:Path):
    ui.link("New notes page...", "/new-note")  # can do to external websites instead

    file_toggle = ui.toggle([".txt", ".md"], value=".txt")

    today = datetime.today().strftime("%Y-%m-%d")

    title_input = ui.input(
        label="Title",
        placeholder=f"Notes {today}",
        # on_change=lambda e: result.set_text(f'Title: {e.value}'),
        validation={"Input too long": lambda value: len(value) < 20},
    )
    # result = ui.label()

    text_input = ui.textarea(value="Write your super important notes here...").props(
        "clearable"
    )

    ui.button(
        "Save",
        on_click=lambda: write_note_handler(
            title_input=title_input,
            text_input=text_input,
            output_dir=output_dir,
            db_path=db_path,
            extension=file_toggle.value,
        ),
        icon="create",
    )