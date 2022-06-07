import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post157"
version_tuple = (0, 4, 0, 157)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post157")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post15"
data_version_tuple = (0, 4, 0, 15)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post15")
except ImportError:
    pass
data_git_hash = "7882d20efe4ef6992b5411468a79625df7f715dd"
data_git_describe = "0.4.0-15-g7882d20e"
data_git_msg = """\
commit 7882d20efe4ef6992b5411468a79625df7f715dd
Merge: ae6c7502 6dfaea37
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Jun 7 09:58:29 2022 +0200

    Merge pull request #573 from Silabs-ArjanB/ArjanB_docd
    
    Prevented table scrollbars

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
