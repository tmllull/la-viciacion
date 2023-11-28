import json
import logging
import os

from dotenv import dotenv_values


class Config:
    def __init__(self):
        try:
            # Load .env
            config = dotenv_values(".env")
            self.ADMIN_USERS = json.loads(config["ADMIN_USERS"])
            self.TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
            self.TELEGRAM_GROUP_ID = config["TELEGRAM_GROUP_ID"]
            self.TELEGRAM_ADMIN_CHAT_ID = config["TELEGRAM_ADMIN_CHAT_ID"]
            self.MYSQL_HOST = config["MYSQL_HOST"]
            self.MYSQL_DATABASE = config["MYSQL_DATABASE"]
            self.MYSQL_USER = config["MYSQL_USER"]
            self.MYSQL_PASSWORD = config["MYSQL_PASSWORD"]
            self.CLOCKIFY_BASEURL = config["CLOCKIFY_BASEURL"]
            self.CLOCKIFY_WORKSPACE = config["CLOCKIFY_WORKSPACE"]
            self.CLOCKIFY_ADMIN_API_KEY = config["CLOCKIFY_ADMIN_API_KEY"]
            self.RAWG_URL = config["RAWG_URL"]
            self.START_DATE = config["START_DATE"]
            self.INVITATION_KEY = config["INVITATION_KEY"]
            self.API_KEY = config["API_KEY"]
            self.SECRET_KEY = config["SECRET_KEY"]
            self.ACCESS_TOKEN_EXPIRE_MINUTES = config["ACCESS_TOKEN_EXPIRE_MINUTES"]
            self.CORS_ORIGINS = json.loads(config["CORS_ORIGINS"])

        except Exception:
            self.TELEGRAM_GROUP_ID = os.environ["TELEGRAM_GROUP_ID"]
            self.ADMIN_USERS = json.loads(os.environ["ADMIN_USERS"])
            self.TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
            self.TELEGRAM_ADMIN_CHAT_ID = os.environ["TELEGRAM_ADMIN_CHAT_ID"]
            self.MYSQL_HOST = os.environ["MYSQL_HOST"]
            self.MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
            self.MYSQL_USER = os.environ["MYSQL_USER"]
            self.MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
            self.CLOCKIFY_BASEURL = os.environ["CLOCKIFY_BASEURL"]
            self.CLOCKIFY_WORKSPACE = os.environ["CLOCKIFY_WORKSPACE"]
            self.CLOCKIFY_ADMIN_API_KEY = os.environ["CLOCKIFY_ADMIN_API_KEY"]
            self.RAWG_URL = os.environ["RAWG_URL"]
            self.START_DATE = os.environ["START_DATE"]
            self.INVITATION_KEY = os.environ["INVITATION_KEY"]
            self.API_KEY = os.environ["API_KEY"]
            self.SECRET_KEY = os.environ["SECRET_KEY"]
            self.ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
            self.CORS_ORIGINS = json.loads(os.environ["CORS_ORIGINS"])

        self.silent = False
