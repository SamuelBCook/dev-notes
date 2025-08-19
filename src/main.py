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

    HOME_NAME = "Home"
    NOTES_NAME = "New Note"
    FIND_NAME = "Find"
    SETTINGS_NAME = "Settings"
    LINKS_NAME = "Links"

    with ui.tabs() as tabs:
        ui.tab(HOME_NAME, icon="home").classes('w-30')
        ui.tab(NOTES_NAME, icon="create").classes('w-30')
        ui.tab(FIND_NAME, icon="explore").classes('w-30')
        ui.tab(SETTINGS_NAME, icon="settings").classes('w-30')
        ui.tab(LINKS_NAME, icon="launch").classes('w-30')

    # Links tab
    with ui.tab_panels(tabs, value=LINKS_NAME):
        with ui.tab_panel(LINKS_NAME):
            links_main(settings_path=settings_path)

    with ui.tab_panels(tabs, value=FIND_NAME):
        with ui.tab_panel(FIND_NAME):
            find_main(db_path=db_path)

    with ui.tab_panels(tabs, value=SETTINGS_NAME):
        with ui.tab_panel(SETTINGS_NAME):
            settings_main()
           
    with ui.tab_panels(tabs, value=NOTES_NAME):
        with ui.tab_panel(NOTES_NAME):
            with ui.column().style('flex: 1; width: 100vw; height: 100vh; gap: 10px'):
                notes_main(output_dir=output_dir, db_path=db_path)

    with ui.tab_panels(tabs, value=HOME_NAME):
        with ui.tab_panel(HOME_NAME):
            home_main()

    ui.run(native=True, reload=False)


if __name__ == "__main__":

    main()
