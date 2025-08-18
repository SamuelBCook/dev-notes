from nicegui import ui, Tailwind
from init_config import init_main
from settings import settings_main
from notes import notes_main
from links import links_main
from find import find_main
from home import home_main
"""
Have README on first page, then meme of the day, then settings and notes page links
Store settings in JSON
TODO:
 - Add tags
 - Add todo
 - Add markdown preview for notes
 - remove filepath from table showing notes
 - add abiltiy to view and edit settings json?
"""

@ui.page("/home")
def main():

    _, output_dir, db_path, settings_path = init_main()

    with ui.tabs() as tabs:
        ui.tab("Home", icon="home").classes('w-30')
        ui.tab("Notes", icon="create").classes('w-30')
        ui.tab("Settings", icon="settings").classes('w-30')
        ui.tab("Find", icon="explore").classes('w-30')
        ui.tab("Links", icon="launch").classes('w-30')

    # Links tab
    with ui.tab_panels(tabs, value="Links"):
        with ui.tab_panel("Links"):
            links_main(settings_path=settings_path)

    with ui.tab_panels(tabs, value="Find"):
        with ui.tab_panel("Find"):
            find_main(db_path=db_path)

    with ui.tab_panels(tabs, value="Settings"):
        with ui.tab_panel("Settings"):
            settings_main()
           
    with ui.tab_panels(tabs, value="Notes"):
        with ui.tab_panel("Notes"):
            with ui.column().style('flex: 1; width: 100vw; height: 100vh; gap: 10px'):
                notes_main(output_dir=output_dir, db_path=db_path)
                    # with ui.row().style('flex: 1; gap: 10px; width: 100%'):
                    #     ui.textarea(label='Textarea 1', placeholder='Type something...').style('flex: 1; height: 100%;')
                    #     ui.textarea(label='Textarea 2', placeholder='Type something...').style('flex: 1; height: 100%;')

    with ui.tab_panels(tabs, value="Home"):
        with ui.tab_panel("Home"):
            home_main()

    ui.run(native=True, reload=False)


@ui.page(
    "/new-note"
)  # can add params like this: ui.page('/new-note/{id}') then have params in func def and use
def new_note():
    # Could add new note stuff here and link back
    # ui.button("TO GITLAB!", on_click=lambda : ui.open('https://gitlab.com/dashboard/projects/member'))
    pass


if __name__ == "__main__":

    main()
