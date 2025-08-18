from nicegui import ui

# Create a row to hold elements side by side
with ui.row():
    # First textarea
    ui.textarea(label='Textarea 1', placeholder='Type something here...')
    
    # Second textarea
    ui.textarea(label='Textarea 2', placeholder='Type something here...')

ui.run()