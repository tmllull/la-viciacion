import json
import logging
import os

from dotenv import dotenv_values


class Config:
    def __init__(self, silent: bool = False):
        try:
            self.ALLOWED_USERS = json.loads(os.environ["ALLOWED_USERS"])
            self.ALLOWED_USERS_RESET = json.loads(os.environ["ALLOWED_USERS_RESET"])
            self.TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
            self.ADMIN_USERS = json.loads(os.environ["ADMIN_USERS"])
            self.TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
            self.TELEGRAM_ADMIN_CHAT_ID = os.environ["TELEGRAM_ADMIN_CHAT_ID"]
            self.GOOGLE_DRIVE_URL = os.environ["GOOGLE_DRIVE_URL"]
            self.DB_HOST = os.environ["DB_HOST"]
            self.DB_NAME = os.environ["DB_NAME"]
            self.DB_USER = os.environ["DB_USER"]
            self.DB_PASS = os.environ["DB_PASS"]
            self.CLOCKIFY_BASEURL = os.environ["CLOCKIFY_BASEURL"]
            self.CLOCKIFY_USERS = json.loads(os.environ["CLOCKIFY_USERS"])
            self.CLOCKIFY_USERS_API = json.loads(os.environ["CLOCKIFY_USERS_API"])
            self.CLOCKIFY_WORKSPACE = os.environ["CLOCKIFY_WORKSPACE"]
            self.DB_MODE = os.environ["DB_MODE"]
            self.N8N_BASE_URL = os.environ["N8N_BASE_URL"]
            self.N8N_WH_ADD_GAME = os.environ["N8N_WH_ADD_GAME"]
            self.HEALTHCHECKS = os.environ["HEALTHCHECKS"]
            self.CLOCKIFY_ADMIN_API_KEY = os.environ["CLOCKIFY_ADMIN_API_KEY"]

        except Exception:
            # Load .env
            config = dotenv_values(".env")
            self.ALLOWED_USERS = json.loads(config["ALLOWED_USERS"])
            self.ALLOWED_USERS_RESET = json.loads(config["ALLOWED_USERS_RESET"])
            self.ADMIN_USERS = json.loads(config["ADMIN_USERS"])
            self.TELEGRAM_TOKEN = config["TELEGRAM_TOKEN"]
            self.GOOGLE_DRIVE_URL = config["GOOGLE_DRIVE_URL"]
            self.TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
            self.TELEGRAM_ADMIN_CHAT_ID = config["TELEGRAM_ADMIN_CHAT_ID"]
            self.DB_HOST = config["DB_HOST"]
            self.DB_NAME = config["DB_NAME"]
            self.DB_USER = config["DB_USER"]
            self.DB_PASS = config["DB_PASS"]
            self.CLOCKIFY_BASEURL = config["CLOCKIFY_BASEURL"]
            self.CLOCKIFY_USERS = json.loads(config["CLOCKIFY_USERS"])
            self.CLOCKIFY_USERS_API = json.loads(config["CLOCKIFY_USERS_API"])
            self.CLOCKIFY_WORKSPACE = config["CLOCKIFY_WORKSPACE"]
            self.DB_MODE = config["DB_MODE"]
            self.N8N_BASE_URL = config["N8N_BASE_URL"]
            self.N8N_WH_ADD_GAME = config["N8N_WH_ADD_GAME"]
            self.HEALTHCHECKS = config["HEALTHCHECKS"]
            self.CLOCKIFY_ADMIN_API_KEY = config["CLOCKIFY_ADMIN_API_KEY"]
        self.TAG_USERS = "Users"
        self.TAG_RANKINGS = "Rankings"
        self.TAG_ACHIEVEMENTS = "Achievements"
        self.silent = silent
