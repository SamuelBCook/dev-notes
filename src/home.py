from nicegui import ui
from pathlib import Path
from loguru import logger
import random

def home_main():
    with open("README.md") as md_f:
            ui.markdown(md_f.read())

            # Use ui.html() to add custom html
            ui.label('Meme of the day:').tailwind('drop-shadow', 'font-bold', 'text-green-600')
            pick_meme()
            

            # mermaid for different types of diagrams
            # ui.mermaid(
            #         """
            #         graph TD;
            #             A[Start] --> B{Is it?};
            #             B -- Yes --> C[OK];
            #             B -- No  --> D[Not OK];
            #         """,
            #         )


def pick_meme(folder_path: Path = Path("/home/samuel-cook/Documents/Meme Stash/")):

    jpg_files = [f for f in folder_path.glob("*.jpg")] + [f for f in folder_path.glob("*.JPG")]

    if not jpg_files:
        logger.warning(f"No memes found in: {folder_path}")

    else:
        random_file = random.choice(jpg_files)
        ui.image(random_file)  # can also use web address to display an image