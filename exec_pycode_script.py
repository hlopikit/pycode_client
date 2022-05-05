import sys

from pycode_context import pycode_context
from helpers import call_pycode_method, is_serializable

import reusable


def make_pycode_env(secret, domain, auth_token, args, request_data):
    if not isinstance(args, list):
        args = []

    pycode_context.set(
        secret=secret,
        domain=domain,
        auth_token=auth_token,
    )

    return dict(
        pycode=reusable,
        pycode_request_data=request_data,
        _pycode_args=args,
        _pycode_result=None,
    )


def add_pycode_function_call_statement(code: str) -> str:
    return '''{}
_pycode_result = main(*_pycode_args)
'''.format(code)


def process_task(task, secret):
    code = add_pycode_function_call_statement(task['code'])
    env = make_pycode_env(
        secret=secret,
        domain=task['domain'],
        auth_token=task['auth_token'],
        args=task['args'],
        request_data=task['request_data'],
    )

    try:
        exec(code, env)
        is_success = True
        error = None

    except Exception as exc:
        is_success = False
        error = '{}: {}'.format(type(exc).__name__, exc)

    result = env['_pycode_result']
    if not is_serializable(result):
        print('Result is not serializable for task {}: {}'.format(task['id'], result))
        result = None
        is_success = False
        error = 'The return value is not JSON serializable'

    set_result_response = call_pycode_method(
        method='set_pycode_task_result',
        secret=secret,
        data=dict(
            secret=secret,
            task_id=task['id'],
            is_success=is_success,
            result=result,
            error=error,
        ),
    )

    if not (set_result_response.ok and set_result_response.json()['ok']):
        is_success = False
        print('Failed to set result for task {}!'.format(task['id']))

    return is_success


def process_activities(secret):
    processed = errors = 0
    while True:
        try:
            response = call_pycode_method(method='get_pycode_task', secret=secret)
            task = response.json()['task']

        except Exception as exc:
            print('Failed to get task: {}'.format(exc))
            break

        if task is None:
            break

        is_success = process_task(task, secret)
        processed += 1
        if not is_success:
            errors += 1

    print('Task processed: {}, errors: {}'.format(processed, errors))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        process_activities(secret=sys.argv[1])

    else:
        print('bad params: {}'.format(sys.argv or '(empty)'))
