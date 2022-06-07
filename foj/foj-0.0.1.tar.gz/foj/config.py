import os, json


class SubmitConfig:
    def __init__(self, files=None, server=None):
        if files is None:
            files = {}
        self.files = files
        self.server = server

    @classmethod
    def check_valid(self):
        return os.path.exists('./submit_config.json') and not os.path.isdir('./submit_config.json')

    @classmethod
    def from_file(cls):
        if not SubmitConfig.check_valid():
            print('submit_config.json is not valid. Stop.')
        with open('./submit_config.json') as f:
            config = json.load(f)
        output = SubmitConfig()
        for c in config:
            output.__dict__[c] = config[c]
        return output



class JudgeConfig:
    def __init__(self):
        pass