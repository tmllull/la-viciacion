import datetime
import json

import requests

from ..config import Config
from . import logger
from . import my_utils as utils

config = Config()


class ClockifyApi:
    def __init__(self) -> None:
        self.RESPONSE_OK = 0
        self.ERROR_TIMER_ACTIVE = 1
        self.GENERIC_ERROR = 2
        self.USER_NOT_EXISTS = 3
        self.API_USER_NOT_ADDED = 4
        self.GET = "GET"
        self.POST = "POST"
        self.PATCH = "PATCH"

    def send_clockify_request(self, method, endpoint, data, api_key):
        if api_key is None and api_key != config.CLOCKIFY_ADMIN_API_KEY:
            return self.API_USER_NOT_ADDED
        else:
            url = "{0}{1}".format(config.CLOCKIFY_BASEURL, endpoint)
            headers = {"X-API-KEY": api_key}
            payload = data
            try:
                if payload is not None:
                    request = requests.request(
                        method, url, headers=headers, json=payload
                    )
                else:
                    request = requests.request(method, url, headers=headers)
            except Exception as e:
                logger.info("Error on send request on clockify")
                exit(e)

            if not request.ok:
                logger.debug(
                    "Error({}): {}".format(request.status_code, request.content)
                )
            return request

    def add_project(self, project_name):
        method = self.POST
        data = {"name": project_name}
        endpoint = "/workspaces/{}/projects".format(config.CLOCKIFY_WORKSPACE)
        response = self.send_clockify_request(
            method, endpoint, data, config.CLOCKIFY_ADMIN_API_KEY
        )
        return response.json()

    def get_project_by_id(self, project_id) -> json:
        method = self.GET
        endpoint = "/workspaces/{}/projects/{}".format(
            config.CLOCKIFY_WORKSPACE, project_id
        )
        response = self.send_clockify_request(
            method, endpoint, None, config.CLOCKIFY_ADMIN_API_KEY
        )
        return response.json()

    def get_project_by_name(self, project_name) -> json:
        method = self.GET
        endpoint = "/workspaces/{}/projects?name={}&strict-name-search=true".format(
            config.CLOCKIFY_WORKSPACE, project_name
        )
        response = self.send_clockify_request(
            method, endpoint, None, config.CLOCKIFY_ADMIN_API_KEY
        )
        return response.json()

    def get_project_id_by_strict_name(self, game_name, api_key):
        if api_key is None:
            return self.API_USER_NOT_ADDED
        else:
            method = self.GET
            endpoint = (
                "/workspaces/{0}/projects?name={1}&strict-name-search=true".format(
                    config.CLOCKIFY_WORKSPACE, game_name
                )
            )
            data = None
            response = self.send_clockify_request(method, endpoint, data, api_key)
            if response.status_code == 200 and len(response.json()) > 0:
                return response.json()[0].get("id")
            else:
                Exception(game_name + " not exists")

    def send_clockify_timer_request(self, action, user_id, game_name, api_key):
        method = None
        data = None
        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        user = ""  # TODO: migrate to DB. config.CLOCKIFY_USERS.get(user_id)
        if api_key is None:
            return self.API_USER_NOT_ADDED
        else:
            if user is not None:
                endpoint = "/workspaces/{}/user/{}/time-entries".format(
                    config.CLOCKIFY_WORKSPACE, user
                )
                if action == "start":
                    project_id = self.get_project_id_by_strict_name(game_name, api_key)
                    method = self.POST
                    data = {
                        "start": now,
                        "description": "new time register for " + game_name,
                        "billable": "false",
                        "projectId": project_id,
                    }
                elif action == "stop":
                    method = self.PATCH
                    data = {
                        "end": now,
                    }
            else:
                return self.USER_NOT_EXISTS
            response = self.send_clockify_request(method, endpoint, data, api_key)
            # TODO add more handles (if needed)
            if response.status_code == 404 and action == "stop":
                return self.ERROR_TIMER_ACTIVE
            elif response.status_code == 200 or response.status_code == 201:
                return self.RESPONSE_OK
            else:
                return self.GENERIC_ERROR

    def active_clockify_timer(self, game_name, user_id):
        # TODO: TBI
        return "TBI"
        return self.send_clockify_timer_request(
            "start", user_id, game_name, config.CLOCKIFY_USERS_API.get(user_id)
        )

    def stop_active_clockify_timer(self, user_id):
        # TODO: TBI
        return "TBI"
        return self.send_clockify_timer_request(
            "stop", user_id, None, config.CLOCKIFY_USERS_API.get(user_id)
        )

    def get_time_entries(self, clockify_user_id, start_date=None):
        if clockify_user_id is None or not utils.check_hex(clockify_user_id):
            return []
        # start must be in format yyyy-MM-ddThh:mm:ssZ
        try:
            if start_date is None:
                date = datetime.datetime.now()
                date = date.replace(hour=0, minute=0, second=0)
                start = date - datetime.timedelta(days=1)
                start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
            else:
                date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                start = date - datetime.timedelta()
                start = start.strftime("%Y-%m-%dT%H:%M:%SZ")
            page = 0
            entries = []
            has_entries = True
            while has_entries:
                page += 1
                endpoint = "/workspaces/{}/user/{}/time-entries?page-size=500&page={}&start={}".format(
                    config.CLOCKIFY_WORKSPACE, clockify_user_id, page, start
                )
                response = self.send_clockify_request(
                    self.GET, endpoint, None, config.CLOCKIFY_ADMIN_API_KEY
                )
                if len(response.json()) > 0:
                    for entry in response.json():
                        entries.append(entry)
                else:
                    has_entries = False
            return entries
        except Exception as e:
            logger.info("Error getting time entries: " + str(e))
            raise e

    def add_time_entry(self, player, date, time):
        return

    def get_tags(self):
        response = self.send_clockify_request(
            "GET",
            "/workspaces/" + config.CLOCKIFY_WORKSPACE + "/tags",
            None,
            config.CLOCKIFY_ADMIN_API_KEY,
        )
        return response.json()
