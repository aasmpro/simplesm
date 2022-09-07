from collections import namedtuple
from .simplesm import SimpleSM


VersionInfo = namedtuple("VersionInfo", ("major", "minor", "patch"))

VERSION = VersionInfo(0, 1, 3)

__version__ = "{0.major}.{0.minor}.{0.patch}".format(VERSION)
__all__ = [SimpleSM]