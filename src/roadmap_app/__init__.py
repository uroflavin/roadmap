from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("roadmap")
except PackageNotFoundError:
    __version__ = "unknown"

from .cli import main  # noqa: F401
