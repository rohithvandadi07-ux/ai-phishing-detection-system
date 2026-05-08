import time

CACHE = {}

CACHE_DURATION = 300


def get_cached_result(url):

    if url in CACHE:

        result, timestamp = CACHE[url]

        if time.time() - timestamp < CACHE_DURATION:

            return result

    return None


def store_result(url, result):

    CACHE[url] = (result, time.time())