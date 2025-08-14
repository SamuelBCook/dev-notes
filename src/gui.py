from nicegui import ui, Client
from backend import write_note
from db_utils import create_tables, insert_note, select_all_notes
from pathlib import Path
from datetime import datetime
from loguru import logger
import random


'''
Have README on first page, then meme of the day, then settings and notes page links
Store settings in JSON
Add tags and TODO
'''


def write_note_handler(
    title_input: ui.textarea, text_input: ui.textarea, output_dir: Path, db_path: Path
):

    note_uuid = write_note(output_dir=output_dir, note_title=title_input.value, note_text=text_input.value)

    insert_note(
        note_uuid=note_uuid,
        db_path=db_path,
        note_title=title_input.value,
        note_path=output_dir / str(title_input.value),
    )


def create_notes_table(db_path:Path):
    
    notes_df = select_all_notes(db_path=db_path)
    table = ui.table.from_pandas(notes_df, column_defaults={
        'align':'left',
        'headerClasses':'uppercase text-primary',
        'sortable':True
    }).classes('max-h-40')

    return table


def switch_modes(new_mode:str):
    logger.info(f'Switching to mode: {new_mode}')

    dark = ui.dark_mode()

    if new_mode == 'Dark':
        dark.enable()
        


    elif new_mode == 'Light':
        #ui.add_head_html('<style>body {background-color: ##ffabcb; }</style>')
        #ui.dark_mode()

        dark.disable()   


def pick_meme(folder_path: Path = Path('/home/samuel-cook/Documents/Meme Stash/')):

    jpg_files = [f for f in folder_path.glob("*.jpg")] + [f for f in folder_path.glob("*.JPG")]

    if not jpg_files:
        logger.warning(f"No memes found in: {folder_path}")

    else:
        random_file = random.choice(jpg_files)
        ui.image(random_file)  # can also use web address to display an image

def play_video(video_url:str):
    video = ui.video(video_url)
    video.on('ended', lambda _: ui.notify('Video is over'))


@ui.page('/new-note') # can add params like this: ui.page('/new-note/{id}') then have params in func def and use
def new_note():
    # Could add new note stuff here and link back
    #ui.button("TO GITLAB!", on_click=lambda : ui.open('https://gitlab.com/dashboard/projects/member')) 
    pass

@ui.page('/home')
def main():

    OUTPUT_DIR = Path("notes/")
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    DB_DIR = Path("db/")
    DB_DIR.mkdir(exist_ok=True, parents=True)
    DB_PATH = DB_DIR / "dev_notes.db"

    create_tables(db_path=DB_PATH)

    with ui.tabs() as tabs:
        ui.tab('Home',icon='home')
        ui.tab('Notes',icon='create')
        ui.tab('Settings',icon='settings')

    ui.label("Sams Great Note App")

    # Settings tab
    with ui.tab_panels(tabs, value='Settings'):
        with ui.tab_panel('Settings'):
            # TOGGLE
            toggle = ui.toggle(['Light','Dark'], value='Light')
            toggle.on_value_change(callback=lambda: switch_modes(new_mode=toggle.value))

            # SLIDER
            slider = ui.slider(min=0, max=10, value=5)
            ui.label().bind_text_from(slider,'value')

            #ui.avatar('') to add a user image


    with ui.tab_panels(tabs, value='Notes'):
        with ui.tab_panel('Notes'):
            
            ui.link('New notes page...', '/new-note')

            today = datetime.today().strftime("%Y-%m-%d")

            title_input = ui.input(
                label='Title',
                    placeholder=f'Notes {today}',
                    #on_change=lambda e: result.set_text(f'Title: {e.value}'),
                    validation={'Input too long':lambda value: len(value) < 20}
                    )
            #result = ui.label()

            text_input = ui.textarea(value="Write your super important notes here...").props("clearable")

            ui.button(
                "Save",
                on_click=lambda: write_note_handler(
                    title_input=title_input, text_input=text_input, output_dir=OUTPUT_DIR, db_path=DB_PATH
                ),
                icon="create",
            )

            notes_table = create_notes_table(db_path=DB_PATH)

    with ui.tab_panels(tabs, value="Home"):
        with ui.tab_panel('Home'):

            # Open the README and display in UI
            with open('README.md') as md_f:
                ui.markdown(md_f.read())

            
            # Use ui.html() to add custom html

            pick_meme()
            #play_video()

            # mermaid for different types of diagrams
            # ui.mermaid(
            #         """
            #         graph TD;
            #             A[Start] --> B{Is it?};
            #             B -- Yes --> C[OK];
            #             B -- No  --> D[Not OK];
            #         """,
            #         )
        

    ui.run(native=True, reload=False)



if __name__ == "__main__":

    main()
