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
            self.TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
            self.TELEGRAM_ADMIN_CHAT_ID = config["TELEGRAM_ADMIN_CHAT_ID"]
            self.MYSQL_HOST = config["MYSQL_HOST"]
            self.MYSQL_DATABASE = config["MYSQL_DATABASE"]
            self.MYSQL_USER = config["MYSQL_USER"]
            self.MYSQL_PASSWORD = config["MYSQL_PASSWORD"]
            self.CLOCKIFY_BASEURL = config["CLOCKIFY_BASEURL"]
            self.CLOCKIFY_USERS = json.loads(config["CLOCKIFY_USERS"])
            self.CLOCKIFY_USERS_API = json.loads(config["CLOCKIFY_USERS_API"])
            self.CLOCKIFY_WORKSPACE = config["CLOCKIFY_WORKSPACE"]
            self.HEALTHCHECKS = config["HEALTHCHECKS"]
            self.CLOCKIFY_ADMIN_API_KEY = config["CLOCKIFY_ADMIN_API_KEY"]
            self.RAWG_URL = config["RAWG_URL"]

        except Exception:
            self.TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
            self.ADMIN_USERS = json.loads(os.environ["ADMIN_USERS"])
            self.TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
            self.TELEGRAM_ADMIN_CHAT_ID = os.environ["TELEGRAM_ADMIN_CHAT_ID"]
            self.MYSQL_HOST = os.environ["MYSQL_HOST"]
            self.MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
            self.MYSQL_USER = os.environ["MYSQL_USER"]
            self.MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
            self.CLOCKIFY_BASEURL = os.environ["CLOCKIFY_BASEURL"]
            self.CLOCKIFY_USERS = json.loads(os.environ["CLOCKIFY_USERS"])
            self.CLOCKIFY_USERS_API = json.loads(os.environ["CLOCKIFY_USERS_API"])
            self.CLOCKIFY_WORKSPACE = os.environ["CLOCKIFY_WORKSPACE"]
            self.HEALTHCHECKS = os.environ["HEALTHCHECKS"]
            self.CLOCKIFY_ADMIN_API_KEY = os.environ["CLOCKIFY_ADMIN_API_KEY"]
            self.RAWG_URL = os.environ["RAWG_URL"]
