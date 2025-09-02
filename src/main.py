from nicegui import ui, Tailwind, app
from init_config import init_main
from settings import settings_main
from notes import notes_main
from links import links_main
from find import find_main
from home import home_main
from pathlib import Path
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

    app.native.start_args['icon'] = Path('static/gui_icon.ico').absolute()
    app.native.window_args['title'] = "DevNotes"
    app.native.window_args['shadow'] = True
    #app.native.window_args['background_color'] = "#B9BFE4"

    HOME_NAME = "Home"
    NOTES_NAME = "New Note"
    FIND_NAME = "Find"
    SETTINGS_NAME = "Settings"
    LINKS_NAME = "Links"

    PRIMARY_COLOUR = '#7dd3fc'
    SECONDARY_COLOUR = "#eea4e8"

    TABLE_COLOUR = "#cec2db"
    CELL_COLOUR = "#6e6b96"

    # ACCENT_COLOUR = '#'

    ## Global CSS
    '''
    body                # Browser window background  @
    .q-page             # Main page content area  @
    .q-page-container   # Container wrapping page content  @
    .q-layout           # Overall layout container  @
    .q-header           # Header bar  @
    .q-footer           # Footer bar  @
    .q-input__control   # Text input fields  @
    .q-input__control textarea  # Textarea fields  @
    .q-markdown         # Markdown display areas  @
    .q-table            # Table component  @
    .q-table__cell      # Individual table cells  @
    .q-btn              # Buttons  @
    .q-btn__content     # Button text/content
    .q-item             # List items
    .q-item__section    # Sections inside list items
    .q-item__label      # Labels inside list items
    .q-card             # Card container
    .q-card__section    # Card content section
    .q-banner           # Banner messages
    .q-dialog           # Modal/dialog windows
    .q-tooltip          # Tooltip popups
    p                   # Paragraph text
    h1                  # Heading level 1
    h2                  # Heading level 2
    h3                  # Heading level 3
    a                   # Links
    .q-scrollarea__viewport  # Scrollable container viewport
    .q-separator        # Dividers/lines
    '''
    ui.add_head_html(f'''
        <style>
        /* Base page */
        body, .q-page, .q-page-container, .q-layout, .q-header, .q-footer,
        .q-input__control {{
            background-color: {PRIMARY_COLOUR} !important;
        }}
        

        /* Button style */
        .q-btn {{
            background-color: {SECONDARY_COLOUR} !important;
        }}

        /* Table */
        .q-table {{
            background-color: {TABLE_COLOUR} !important;
            }}

        /* Markdown */
        .q-markdown, 
        .q-markdown .q-markdown__content {{
            background-color: {PRIMARY_COLOUR} !important;
        }}
        </style>
        ''')  #  .q-btn, if I want to change buttons


    ''' Does fuck all:

    .q-input__control textarea {{
            background-color: {PRIMARY_COLOUR};
        }}
    .q-table__cell {{
        background-color: {CELL_COLOUR} !important;
        }}
    '''

    #app.native.window_args
    #app.native.window_args['title_bar_color'] = '#7dd3fc'
    #app.native.window_args['title_bar_text_color'] = '#171717'

    #app.native.start_args['width'] = 800
    #app.native.start_args['height'] = 800
        #app.native.window_args['always_on_top'] = True

    root_dir, output_dir, db_path, settings_path = init_main()

    
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
            find_main(db_path=db_path, root_dir=root_dir)

    with ui.tab_panels(tabs, value=SETTINGS_NAME):
        with ui.tab_panel(SETTINGS_NAME):
            settings_main(root_dir=root_dir)
           
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
