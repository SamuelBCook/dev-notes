from nicegui import ui
from loguru import logger

def settings_main():
    # TOGGLE
    darkmode_toggle = ui.toggle(["Light", "Dark"], value="Light")
    darkmode_toggle.on_value_change(
        callback=lambda: switch_modes(new_mode=darkmode_toggle.value)
    )

    # SLIDER
    slider = ui.slider(min=0, max=10, value=5)
    ui.label().bind_text_from(slider, "value")

    # ui.avatar('') to add a user image


def switch_modes(new_mode: str):
    logger.info(f"Switching to mode: {new_mode}")

    dark = ui.dark_mode()

    if new_mode == "Dark":
        dark.enable()

    elif new_mode == "Light":
        # ui.add_head_html('<style>body {background-color: ##ffabcb; }</style>')
        # ui.dark_mode()

        dark.disable()