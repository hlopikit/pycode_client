import json

import requests

from constants import DOMAIN
from django_helpers import DjangoJSONEncoder
from pycode_context import pycode_context


def is_serializable(value):
    try:
        json.dumps(value, cls=DjangoJSONEncoder)
    except (ValueError, TypeError):
        return False

    return True


def call_pycode_method(method, data=None, secret=None):
    if secret is None:
        secret = pycode_context.secret

    if data is not None:
        data = json.dumps(data, cls=DjangoJSONEncoder)

    return requests.post(
        url='https://{}/method/{}/'.format(DOMAIN, method),
        params=dict(secret=secret),
        headers={'Content-Type': 'application/json'},
        data=data,
    )
