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


def get_address_information(node_public_key: str):
    active = "0"
    staked_amount = "0"

    try:
        bids = requests.post("https://node-clarity-testnet.make.services/rpc",
                             json={"jsonrpc": "2.0", "id": "0", "method": "state_get_auction_info",
                                   "params": []}).json()[
            'result']['auction_state']['bids']
    except (Timeout, ConnectionError):
        return active, staked_amount

    for bid in bids:
        if bid['public_key'] == node_public_key:
            active = "0" if bid['bid']['inactive'] else "1"
            staked_amount = bid['bid']['staked_amount']
            break

    return active, staked_amount


def get_additional_info():
    try:
        response = requests.get(url="http://127.0.0.1:8888/status")
    except (Timeout, ConnectionError):
        logging.error("[Node info] Timeout connection")
        return None

    content = response.json()

    public_key = content.get("our_public_signing_key", "None")
    additional_node_info = '{' + f'address="{public_key}"' + '}'

    active, staked_amount = get_address_information(public_key)

    info = f"# HELP block_height\n" \
           f"# TYPE block_height gauge\n" \
           f"block_height{additional_node_info} {content.get('last_added_block_info', dict()).get('height', 0)}\n" \
           f"# HELP era_id\n" \
           f"# TYPE era_id gauge\n" \
           f"era_id{additional_node_info} {content.get('last_added_block_info', dict()).get('era_id', 0)}\n" \
           f"# HELP active\n" \
           f"# TYPE active gauge\n" \
           f"active{additional_node_info} {active}\n" \
           f"# HELP staked_amount\n" \
           f"# TYPE staked_amount gauge\n" \
           f"staked_amount{additional_node_info} {staked_amount}\n"

    return info
