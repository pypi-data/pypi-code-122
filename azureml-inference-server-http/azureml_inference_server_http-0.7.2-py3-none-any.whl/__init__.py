from ._version import __version__


# Set to true if we setup debugpy in entry.py for users debugging local deployments. This variable is checked in
# `ensure_debugpy.py`, called by gunicorn/run.
_HAS_DEBUGPY_SUPPORT = True
