import requests
from http import HTTPStatus

from app.utils.schemas.router_schemas import RouterSchema

class HTTPService:

    def __init__(self, server: str, router_id: int):
        self._server = server
        self._router_id = router_id

    @property
    def server(self):
        return self._server

    @property
    def router_id(self):
        return self._router_id

    def get_router_info(self) -> RouterSchema:
        response = requests.get(f"{self.server}/api/routers/{self.router_id}")
        if response.status_code != HTTPStatus.OK:
            raise Exception(response)
        return RouterSchema().load(data=response.json())
