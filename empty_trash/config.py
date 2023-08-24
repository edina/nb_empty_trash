import os

from traitlets import Bool, Dict, Float, Int, List, TraitType, Unicode, Union, default
from traitlets.config import Configurable

try:
    # Traitlets >= 4.3.3
    from traitlets import Callable
except ImportError:
    from .utils import Callable


class ResourceUseDisplay(Configurable):
    """
    Holds server-side configuration for nbresuse
    """

    disk_limit = Union(
        trait_types=[Int(), Callable()],
        default_value=0,
        help="""
        Disk usage limit to display to the user.

        Note that this does not actually limit the user's Disk space!

        Defaults to reading from the `DISK_LIMIT` environment variable. If
        set to 0, the total partition space available is displayed.
        """,
    ).tag(config=True)

    @default("disk_limit")
    def _disk_limit_default(self):
        return int(os.environ.get("DISK_LIMIT", 0))

    disk_dir = Union(
        trait_types=[Unicode(), Callable()],
        default_value=os.getcwd(),
        help="""
        The "home" directory

        Defaults to reading from the `DISK_DIR` environment variable. If
        not defined, it defaults to $HOME.
        """,
    ).tag(config=True)

    @default("disk_dir")
    def _disk_dir_default(self):
        return str(os.environ.get("DISK_DIR", os.getcwd()))
