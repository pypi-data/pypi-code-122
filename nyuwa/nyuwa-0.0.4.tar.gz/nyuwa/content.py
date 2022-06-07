# constant.py
class _content:
    # class ContentError(TypeError):
    #     pass
    # class ConstCaseError(ConstError):
    #     pass

    def __setattr__(self, name, value):
        # if name in self.__dict__:
        #     raise self.ConstError("Can't change const.{}".format(name))
        # if not name.isupper():
        #     raise self.ConstCaseError("const name {} is not all uppercase".format(name))
        self.__dict__[name] = value

import sys
# print(__name__) #constant
sys.modules[__name__] = _content()

### TODO 想做一个  单例