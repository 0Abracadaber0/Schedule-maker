import os

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


class Settings:

    def __init__(self):
        load_dotenv()

        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.DATABASE_URI = os.getenv('DATABASE_URI')
        self.ALGORITHM = os.getenv('ALGORITHM')

        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.REDIRECT_URI = os.getenv('REDIRECT_URI')

        self.static_files = StaticFiles(directory='/home/azazel/Schedule-maker/Schedule_maker/static')
        self.templates = Jinja2Templates('templates')

        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


settings = Settings()
