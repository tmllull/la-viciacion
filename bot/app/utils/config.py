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
            self.DB_MODE = config["DB_MODE"]
            self.N8N_BASE_URL = config["N8N_BASE_URL"]
            self.N8N_WH_ADD_GAME = config["N8N_WH_ADD_GAME"]
            self.CLOCKIFY_ADMIN_API_KEY = config["CLOCKIFY_ADMIN_API_KEY"]
            self.API_URL = config["API_URL"]

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
            self.API_URL = os.environ["API_URL"]
