from db_utils import init_db_config
from loguru import logger
from pathlib import Path
from classes import DefaultSettings
import json
from pathlib import Path
from platformdirs import user_data_dir

def init_main() -> tuple[Path, Path, Path, Path]:

    # TODO: check if already exists

    logger.info("Initialising Dev Notes App...")

    root_dir = init_app_dir()

    output_dir, db_path = init_other_dirs(root_dir)

    init_db_config(db_path=db_path)

    settings_path = init_settings_config(root_path=root_dir)

    # TODO: if fails rollback and delete all

    logger.info("Dev Notes App initialised successfully!")

    return root_dir, output_dir, db_path, settings_path


def init_app_dir():

    app_name = "DevNotes"
    app_author = "SamuelCook"

    root_dir = Path(user_data_dir(app_name, app_author))
    logger.info(f"Root dir: {root_dir}")
    root_dir.mkdir(parents=True, exist_ok=True)
    return root_dir



def init_settings_config(root_path: Path):

    settings_path = root_path / "settings.json"
    if settings_path.exists():
        logger.debug("Settings file already exists")
        return settings_path

    default_settings = {
        'logos':{
        link.name: {"url": link.url, "img": link.img, "width": link.width}
        for link in DefaultSettings.logo_data
    }
    }
    
    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(default_settings, f, indent=4)

    logger.debug("Default settings written")
    return settings_path


def init_other_dirs(root_dir:Path):

    OUTPUT_DIR = root_dir / "notes"
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    DB_DIR = root_dir / "db"
    DB_DIR.mkdir(exist_ok=True, parents=True)
    DB_PATH = DB_DIR / "dev_notes.db"

    return OUTPUT_DIR, DB_PATH
