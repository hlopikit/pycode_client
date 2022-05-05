from helpers import call_pycode_method


class PycodeValueError(ValueError):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return str(self.response.status_code)


class GetValueError(PycodeValueError):
    pass


class SetValueError(PycodeValueError):
    pass


def validate_key(key):
    if not isinstance(key, str):
        raise ValueError('key must be a string')

    if len(key) > 255:
        raise ValueError('max key length is 255')


def get_value(key):
    validate_key(key)

    response = call_pycode_method(method='storage/get_value', data=dict(key=key))
    if response.ok:
        return response.json()['value']

    raise GetValueError(response)


def set_value(key, value):
    validate_key(key)

    response = call_pycode_method(method='storage/set_value', data=dict(key=key, value=value))
    if response.ok:
        return response.json()['ok']

    raise SetValueError(response)
