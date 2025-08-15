from nicegui import ui 
from loguru import logger
from backend import read_settings, overwrite_settings
from pathlib import Path

def links_main(settings_path: Path):
            
    settings = read_settings(settings_path)

    # Create a grid container (we'll update this later)
    grid = ui.element().classes(
        "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 justify-items-center items-center"
    )

    # Function to refresh grid
    def refresh_grid():
        logger.debug('Refreshing grid')
        grid.clear()
        for logo in settings["logos"].values():
            with grid:
                with ui.link(target=logo["url"], new_tab=True):
                    ui.image(logo["img"]).style(f'width:{logo["width"]}; cursor:pointer;')

    # Dialog for adding a new logo
    with ui.dialog() as new_logo_dialog, ui.card():
        ui.label("Add a New Link")
        name_input = ui.input("Name")
        url_input = ui.input("URL")
        img_input = ui.input("Image URL")

        with ui.row():
            ui.button("Cancel", on_click=new_logo_dialog.close)

            def add_logo():
                logger.debug('Opening new link dialog')
                settings['logos'][name_input.value] = {
                        "url": url_input.value,
                        "img": img_input.value,
                        "width": "150px",  # default width
                    }
                refresh_grid()
                new_logo_dialog.close()
                overwrite_settings(settings_path, settings)
                logger.debug('New link added')

            ui.button("Add", on_click=add_logo).props("color=primary")

    # Button to open the dialog
    ui.button("Add Your Own Link", on_click=new_logo_dialog.open).props("color=accent")

    # First render
    refresh_grid()