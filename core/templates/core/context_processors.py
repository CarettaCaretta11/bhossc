import os


def root_url_processor():
    root_url = os.environ["BHOSSC_ROOT_URL"]
    return {'root_url': root_url}