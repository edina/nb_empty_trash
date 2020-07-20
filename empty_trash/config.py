import os

from traitlets import Bool
from traitlets import default
from traitlets import Dict
from traitlets import Float
from traitlets import Int
from traitlets import List
from traitlets import TraitType
from traitlets import Unicode
from traitlets import Union
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

    trash_dir = Union(
        trait_types=[Unicode(), Callable()],
        default_value=os.getcwd(),
        help="""
        The directory that the notebook copies Trash to on deletion

        Defaults to reading from the `TRASH_DIR` environment variable. If
        not defined, it effectively defaults to $HOME/.local/share/Trash/
        """,
    ).tag(config=True)

    @default("trash_dir")
    def _trash_dir_default(self):
        return str(
            os.environ.get(
                "TRASH_DIR",
                os.path.join(
                    os.environ.get("HOME", os.getcwd()), ".local/share/Trash/"
                ),
            )
        )

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
        return str(os.environ.get("DISK_DIR", os.environ.get("HOME", os.getcwd())))
