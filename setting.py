import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LBA = os.environ.get("LINE_BOT_API_KEY")
HANDLER = os.environ.get("HANDLER")