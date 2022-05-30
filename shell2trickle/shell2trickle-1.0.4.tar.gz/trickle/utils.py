import argparse
from uuid import uuid4


def parseArgs():
    # 获取脚本参数
    ap = argparse.ArgumentParser(
        prog="trickle",
        description="Post your trickle by shell"
    )
    ap.add_argument("send", type=str, nargs="+", help="your trickle content")
    ap.add_argument("-e", "--endpoint", type=str, default="", help="trickle intg endpoint")
    ap.add_argument("-t", "--token", type=str, default='', help="your trickle account token")

    args = vars(ap.parse_args())
    return args


def get_uuid():
    return str(uuid4())


def generateBlock(text: str):
    return {
        "id": get_uuid(),
        "type": "rich_texts",
        "blocks": [],
        "indent": 0,
        "display": "block",
        "isFirst": True,
        "elements": [{
            "id": get_uuid(),
            "text": text,
            "type": "text",
            "elements": [],
            "isCurrent": True
        }],
        "isCurrent": False
    }


def newline():
    return generateBlock(text="")

    
def content2Blocks(content: str):
    blocks = []

    paragraphs = content.split("\\n")
    for idx, para in enumerate(paragraphs):
        blocks.append(generateBlock(text=para.strip()))
        if idx != len(paragraphs)-1:
            blocks.append(newline())

    return blocks