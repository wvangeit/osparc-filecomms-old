from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("osparc_filecomms")
except PackageNotFoundError:
    # package is not installed
    pass

from . import handshakers  # NOQA
