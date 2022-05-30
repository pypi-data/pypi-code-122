from trickle.utils import get_uuid, content2Blocks
import requests


class TrickleSendFailed(Exception):
    pass


def sendTrickle(content: str, endpoint: str, token: str):
    blocks = content2Blocks(content)
    resp = requests.post(
        url=endpoint, 
        json={"blocks": blocks}, 
        headers={"Authorization": token}
    )

    if resp.status_code != 201:
        raise TrickleSendFailed(f"Your trickle send failed: {resp.json()}")
    
    print("Sended Successfully!")
