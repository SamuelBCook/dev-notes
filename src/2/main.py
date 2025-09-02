from nicegui import ui, Tailwind, app
from pathlib import Path
import uuid


"""
This way it uses the same UUID - need to apply this to the actual page
"""
@ui.page("/home")
def main():

    app.native.start_args['icon'] = Path('static/gui_icon.ico').absolute()
    app.native.window_args['title'] = "DevNotes"
    app.native.window_args['shadow'] = True

    text_input = ui.textarea(label='New Note', placeholder='Type something...').style('flex: 1; height: 100%;')
    text_input.uuid = uuid.uuid4()

    save_button = ui.button(
                "Save",
                on_click=lambda: print(text_input.uuid),
                icon="create",
            )
    
    def reset_input():
        text_input.uuid = uuid.uuid4()
        text_input.value = None
    
    new_button = ui.button("New", icon="refresh", on_click=lambda:  reset_input())


    ui.run(native=True, reload=False)


if __name__ == "__main__":

    main()
