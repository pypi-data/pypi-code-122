import os
from zipfile import ZipFile
from foj.config import SubmitConfig
from os.path import join as pjoin
from os.path import relpath as prel

submit_config_text = '''{
    "files": {},
    "server": "0.0.0.0:8000"
}
'''

def zip_package(files):
    if os.path.exists('foj-submit/submit.zip'):
        os.remove('foj-submit/submit.zip')
    with ZipFile('foj-submit/submit.zip', mode='w') as z:
        for arc_root,real_file in files.items():
            z.write(filename=real_file, arcname=arc_root)
            if os.path.isdir(real_file):
                for real_root, pure_paths, pure_names in os.walk(real_file):
                    arc_mid = prel(real_root, real_file)
                    for pure_path in pure_paths:
                        z.write(filename=pjoin(real_root, pure_path), arcname=pjoin(arc_root, arc_mid, pure_path))
                    for pure_name in pure_names:
                        z.write(filename=pjoin(real_root, pure_name), arcname=pjoin(arc_root, arc_mid, pure_name))
        z.write(filename='submit_config.json', arcname='submit_config.json')


class Submitter:
    def __init__(self):
        pass

    def init(self):
        if os.path.exists('./submit_config.json'):
            print('submit_config.json already exists, skip.')
        else:
            with open('submit_config.json', mode='w', encoding='utf-8') as f:
                f.write(submit_config_text)

        if os.path.exists('./foj-submit'):
            print('foj-submit already exists, skip.')
        else:
            os.mkdir('foj-submit')


    def package(self):
        config = SubmitConfig.from_file()
        zip_package(config.files)

    def submit(self):
        pass