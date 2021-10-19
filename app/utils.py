import logging

import requests
from requests.exceptions import Timeout, ConnectionError


def get_prometheus_info(name, url):
    try:
        response = requests.get(url=url)
        return response.text
    except (Timeout, ConnectionError):
        logging.error(f"[{name}] Timeout connection")
        return None


def get_additional_info():
    try:
        response = requests.get(url="http://127.0.0.1:8888/status")
    except (Timeout, ConnectionError):
        logging.error("[Node info] Timeout connection")
        return None

    content = response.json()

    additional_node_info = '{' + f'address="{content.get("our_public_signing_key", "None")}"' + '}'

    info = f"# HELP block_height\n" \
           f"# TYPE block_height gauge\n" \
           f"block_height{additional_node_info} {content.get('last_added_block_info', dict()).get('height', 0)}\n" \
           f"# HELP era_id\n" \
           f"# TYPE era_id gauge\n" \
           f"era_id{additional_node_info} {content.get('last_added_block_info', dict()).get('era_id', 0)}\n"

    return info
