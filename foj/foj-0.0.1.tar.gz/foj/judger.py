import os
from zipfile import ZipFile
from os.path import join as pjoin
from os.path import relpath as prel


judge_config_text = '''{
    "files": {},
    "entry": {
        "windows": "echo foj-judge",
        "linux": "echo foj-judge"
    },
    "sandbox": {
        "enabled": true,
        "always_rebuild": true,
        "internet_access": true,
        "exposed_ports": [],
        "timeout": 10000
    },
    "server": "0.0.0.0:8000"
}
'''

def zip_package():
    if os.path.exists('foj-judge/judge.zip'):
        os.remove('foj-judge/judge.zip')
    with ZipFile('foj-judge/judge.zip', mode='w') as z:
        for real_root, pure_paths, pure_names in os.walk('.'):
            if prel(real_root, '.') == 'foj-judge': continue
            for pure_path in pure_paths:
                z.write(filename=pjoin(real_root, pure_path), arcname=pjoin(real_root, pure_path))
            for pure_name in pure_names:
                z.write(filename=pjoin(real_root, pure_name), arcname=pjoin(real_root, pure_name))

class Judger:
    def __init__(self):
        pass

    def init(self):
        if os.path.exists('./judge_config.json'):
            print('judge_config.json already exists, skip.')
        else:
            with open('judge_config.json', mode='w', encoding='utf-8') as f:
                f.write(judge_config_text)

        if os.path.exists('./foj-judge'):
            print('foj-judge already exists, skip.')
        else:
            os.mkdir('foj-judge')
        
        if os.path.exists('./foj-report'):
            print('foj-report already exists, skip.')
        else:
            os.mkdir('foj-report')

    def test(self):
        pass

    def mock(self):
        pass

    def package(self):
        zip_package()

    def serve(self):
        pass


