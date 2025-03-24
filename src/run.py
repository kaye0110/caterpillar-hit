import logging
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parents[1]
LOCAL_ENV_FILE = ".env"
result = load_dotenv(dotenv_path=os.path.join(ROOT_DIR, LOCAL_ENV_FILE))

uvicorn_logger = logging.getLogger('uvicorn')
uvicorn_logger.setLevel(logging.ERROR)


def run_uvicorn():
    uvicorn.run(app="application:app", host="0.0.0.0", port=19999, reload=False, workers=4)


if __name__ == "__main__":
    run_uvicorn()
