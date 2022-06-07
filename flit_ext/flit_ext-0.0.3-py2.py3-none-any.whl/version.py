from setuptools_scm import ScmVersion


def local_version(version: ScmVersion):
    return version.format_choice("+{node}", "+{node}.d{time:%Y%m%d}")
