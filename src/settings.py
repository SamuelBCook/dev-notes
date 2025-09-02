from nicegui import ui
from loguru import logger
from shutil import rmtree
from pathlib import Path

def settings_main(root_dir:Path):
    # TOGGLE
    darkmode_toggle = ui.toggle(["Light", "Dark"], value="Light")
    darkmode_toggle.on_value_change(
        callback=lambda: switch_modes(new_mode=darkmode_toggle.value)
    )

    # SLIDER
    slider = ui.slider(min=0, max=10, value=5)
    ui.label().bind_text_from(slider, "value")

    # ui.avatar('') to add a user image

    # RESET

    with ui.dialog() as confirm_dialog, ui.card():
            ui.label('⚠️ Are you sure you want to reset the app? All notes will be lost. You must restart the app for changes to take effect.')
            with ui.row():
                ui.button('Cancel', on_click=confirm_dialog.close)
                ui.button('Delete', color='red', on_click=lambda: (rmtree(root_dir), confirm_dialog.close(), logger.success('Deleted! Please restart.')))


    ui.button('NUKE', on_click=lambda: confirm_dialog)


def switch_modes(new_mode: str):
    logger.info(f"Switching to mode: {new_mode}")

    dark = ui.dark_mode()

    if new_mode == "Dark":
        dark.enable()

    elif new_mode == "Light":
        # ui.add_head_html('<style>body {background-color: ##ffabcb; }</style>')
        # ui.dark_mode()

        dark.disable()


def confirm_delete(root_dir:Path):

    if root_dir.exists():

        with ui.dialog() as dialog, ui.card():
            ui.label('⚠️ Are you sure you want to delete this item?')
            with ui.row():
                ui.button('Cancel', on_click=dialog.close)
                ui.button('Delete', color='red', on_click=lambda: (rmtree(root_dir), dialog.close()))


    else:
        raise FileExistsError('Provided path does not exist!')



