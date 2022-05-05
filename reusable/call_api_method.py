import requests
from api_call import api_call
from pycode_context import pycode_context


class BitrixApiError(Exception):
    def __init__(self, response: requests.Response):
        self.response = response

    def __str__(self) -> str:
        return '[{}][{}] {}'.format(self.status, self.error, self.error_description)

    @property
    def status(self):
        return self.response.status_code

    @property
    def json(self):
        try:
            return self.response.json()
        except ValueError:
            return None

    @property
    def error(self) -> str:
        return self.json['error'] if self.json and 'error' in self.json else 'unknown_error'

    @property
    def error_description(self) -> str:
        return self.json.get('error_description', '') if self.json else self.response.content


def call_api_method(api_method, params=None):
    response = api_call(
        domain=pycode_context.domain,
        api_method=api_method,
        auth_token=pycode_context.auth_token,
        params=params,
    )

    if response.ok:
        try:
            return response.json()
        except ValueError:
            pass

    raise BitrixApiError(response)
