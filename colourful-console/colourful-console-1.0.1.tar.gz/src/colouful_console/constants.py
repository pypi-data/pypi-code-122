from re import compile

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

PATTERNS = {
    compile('<w>(.*?)</w>'): WHITE,
    compile('<b>(.*?)</b>'): BLUE,
    compile('<r>(.*?)</r>'): RED,
    compile('<c>(.*?)</c>'): CYAN,
    compile('<g>(.*?)</g>'): GREEN,
    compile('<m>(.*?)</m>'): MAGENTA,
    compile('<y>(.*?)</y>'): YELLOW,
    compile('<ul>(.*>)</ul>'): UNDERLINE
}

TAGS = [
    '<w>', '</w>',
    '<b>', '</b>',
    '<c>', '</c>',
    '<r>', '</r>',
    '<g>', '</g>',
    '<m>', '</m>',
    '<y>', '</y>',
    '<ul>', '</ul>',
]