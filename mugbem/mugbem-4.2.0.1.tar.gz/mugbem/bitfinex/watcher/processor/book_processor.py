import datetime
import struct
import time
from io import BytesIO

from .base.abstract_processor import AbstractProcessor


class BookProcessor(AbstractProcessor):
    def __init__(self, output_file_path, pack_format):
        super(BookProcessor, self).__init__()
        self.output_file_path = output_file_path
        self.pack_format = pack_format

    def handle(self, message, *args, **kwargs):
        if type(message) is list:
            buff = BytesIO()
            if type(message[1][0]) is list:
                for item in message[1]:
                    try:
                        buff.write(struct.pack(self.pack_format, *item))
                    except Exception as e:
                        print(e, message)
                        raise e
            else:
                if len(message[1]) == 3:
                    try:
                        buff.write(struct.pack(self.pack_format, *message[1]))
                    except Exception as e:
                        print(e, message)
                        raise e
            filename_suffix = \
                datetime.datetime.fromtimestamp(int(time.time()) // 3600 * 3600).strftime('%Y_%m_%d_%H_00')
            with open(f'{self.output_file_path}_{filename_suffix}.osas', 'a+b') as f:
                f.write(buff.getvalue())
