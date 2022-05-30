import tktk.base_enhance.ListFrame
import tktk.base_enhance.LogFrame
#pip install git+https://gitee.com/w-8/tktk.git

class ListFrame(tktk.base_enhance.ListFrame.ListFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class LogFrame(tktk.base_enhance.LogFrame.LogFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


