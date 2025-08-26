from nicegui import ui
from datetime import datetime
from backend import write_note_handler
from pathlib import Path



def notes_main(output_dir:Path, db_path:Path):
    #ui.link("New notes page...", "/new-note")  # can do to external websites instead

    today = datetime.today().strftime("%Y-%m-%d")
    default_title = f"Notes {today}"

    with ui.row().style('gap: 10px; align-items: center;'):
            file_toggle = ui.toggle([".txt", ".md"], value=".txt")
            save_button = ui.button(
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

    title_input = ui.input(
        label="Title",
        value=default_title,
        validation={"Input too long": lambda value: len(value) < 20},
    )

    with ui.row().style('width: 100vw; height: 100vh; gap: 10px'):
        text_input = ui.textarea(label='New Note', placeholder='Type something...').style('flex: 1; height: 100%;')
        markdown_preview = ui.markdown('### Lets write some Markdown! ').style('flex: 1; height: 100%; overflow: auto; white-space: pre-wrap; word-wrap: break-word;')
        markdown_preview.visible = (file_toggle.value == ".md")

        text_input.on_value_change(lambda e: markdown_preview.set_content(text_input.value))

    def update_preview(e):
        markdown_preview.visible = (file_toggle.value == ".md")

    file_toggle.on_value_change(update_preview)