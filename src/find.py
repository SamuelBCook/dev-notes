from pathlib import Path
from db_utils import select_all_notes
from nicegui import ui
from loguru import logger

def find_main(db_path:Path, root_dir:Path):
    notes_table = create_notes_table(db_path=db_path, root_dir=root_dir)


def create_notes_table(db_path: Path, root_dir:Path):

    notes_df = select_all_notes(db_path=db_path)

    hidden_df = notes_df.copy()  #  Preserve to find file paths

    notes_df['File path'] = notes_df['File path'].apply(lambda x: str(Path(x).parent).removeprefix(str(root_dir)))
    notes_df['Created'] = notes_df['Created'].dt.floor('s')  # Floor to the second precision

    notes_df = notes_df[['Title', 'Created', 'File path']]

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
        print(current_file)
        if current_file and current_file.exists():
            current_file.write_text(file_viewer.value, encoding='utf-8') # TODO: check if w or a
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
