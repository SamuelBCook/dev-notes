from pathlib import Path
from db_utils import select_all_notes
from backend import update_find_table, write_note_handler
from nicegui import ui
from loguru import logger
from uuid import UUID

def find_main(db_path:Path, root_dir:Path, output_dir:Path):
    #notes_table = create_notes_table(db_path=db_path, root_dir=root_dir)

    container = ui.column()  # container to hold the table + extras

    def refresh():
        container.clear()
        with container:
            create_notes_table(db_path=db_path, root_dir=root_dir, output_dir=output_dir)

    # build initially
    refresh()

    return refresh  # return refresh function so caller can trigger reload


def create_notes_table(db_path: Path, root_dir:Path, output_dir:Path):

    # TODO create handler for getting table deets and get all notes and all tags then merge

    #notes_df = select_all_notes(db_path=db_path)
    notes_df = update_find_table(db_path=db_path)

    hidden_df = notes_df.copy()  #  Preserve to find file paths and titles

    notes_df['File path'] = notes_df['File path'].apply(lambda x: str(Path(x).parent).removeprefix(str(root_dir)))
    notes_df['Created'] = notes_df['Created'].dt.floor('s')  # Floor to the second precision

    #notes_df = notes_df[['Title', 'Created', 'File path']]

    table = ui.table.from_pandas(
        notes_df,
        column_defaults={
            "align": "left",
            "headerClasses": "uppercase text-primary",
            "sortable": True,
        },
        row_key="Title",
    ).classes("'width: 100vw; max-h-80")

    # Text area under the table (start hidden/empty)
    file_viewer = ui.textarea(
        label='File contents',
        placeholder='Click a row to view note...',
    ).style('width: 100vw; height: 100vh')
    file_viewer.visible = False
    
    current_file: Path | None = None
    
    # Save button
    def save_file():
        nonlocal current_file
        if current_file and current_file.exists():
            logger.debug(f'Current file: {current_file.stem}')
            #current_file.write_text(file_viewer.value, encoding='utf-8') # TODO: check if w or a

            write_note_handler(
                title_input=hidden_df.loc[hidden_df["note_id"] == UUID(current_file.stem), "Title"].iloc[0],
                text_input=file_viewer,
                output_dir=output_dir,
                db_path=db_path,
                extension=current_file.suffix,
                note_uuid=UUID(current_file.stem)
            )
            ui.notify(f'Saved - well done!', color='positive')
        else:
            ui.notify('Something aint right kid', color='negative')

    save_button = ui.button('Save changes', on_click=save_file).props('icon=save')
    save_button.visible = False

    def handle_click(e):
        nonlocal current_file

        _, row_data, _ = e.args  # event info, row data, row_index
        title = row_data['Title']

        # lookup file path in hidden df
        row = hidden_df[hidden_df['Title'] == title].iloc[0]
        file_path = Path(row['File path'])
        print(f'{file_path=}')

        if file_path.exists():
            file_viewer.value = file_path.read_text(encoding='utf-8')
            file_viewer.visible = True
            save_button.visible = True
            current_file = file_path
            logger.debug(f'{current_file=}')
        else:
            file_viewer.value = f'File not found: {file_path}'
            file_viewer.visible = True
            save_button.visible = False
            current_file = None
        
    table.on('rowClick', handle_click)

    return table

#ui.link("New notes page...", "/new-note")  # can do to external websites instead
# @ui.page(
#     "/note/{file_path}"
# )  # can add params like this: ui.page('/new-note/{id}') then have params in func def and use
# def new_note():
#     # Could add new note stuff here and link back
#     # ui.button("TO GITLAB!", on_click=lambda : ui.open('https://gitlab.com/dashboard/projects/member'))
#     pass
