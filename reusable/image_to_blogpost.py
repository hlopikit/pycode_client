import reusable as pycode


def image_to_blogpost(image_url, title=' ', dest='UA'):
    """
    Скачивает картинку по url и делает ее log.blogpost.add
    """

    return pycode.call_api_method('log.blogpost.add', {
        'POST_TITLE': title,
        'POST_MESSAGE': '[B][/B]',
        'FILES': [pycode.get_b64_file(image_url)],
    })['result']
