from typing import Any
import requests
from classes import EplanPart

URL_BASE = "http://127.0.0.1:5000/api/v1"


class APIController:
    def __init__(self, url_base: str = URL_BASE):
        self.url_base = url_base

    def get_parts(self, query, *, additional_params: dict[str, Any] = {}, many=True):
        response = requests.get(
            self.url_base + "/parts" if many else "/part",
            params={"query": query, **additional_params},
        )
        if response.status_code == 500:
            print("API error, retrying")
            response = requests.get(
                self.url_base + "/parts" if many else "/part",
                params={"query": query, **additional_params},
            )
        if not response.status_code == 200:
            return {"message": response.reason}
        try:
            return {"data": response.json()}
        except Exception as er:
            return {"message": str(er)}

    def post_parts(self, parts: list[str]):
        return requests.post(self.url_base + "/eplan/beckhoff", json=parts)
