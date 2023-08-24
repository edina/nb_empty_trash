from tornado import ioloop

from empty_trash.config import ResourceUseDisplay
from empty_trash.metrics import TrashMetricsLoader
from empty_trash.prometheus import PrometheusHandler


def _jupyter_server_extension_paths():
    """
    Set up the server extension for collecting size & emptying Trash
    """
    return [{"module": "empty_trash"}]


def _jupyter_nbextension_paths():
    """
    Set up the notebook extension for displaying the button (and the size of Trash)
    """
    return [
        {
            "section": "tree",
            "dest": "empty_trash",
            "src": "static",
            "require": "empty_trash/trash",
        }
    ]


def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """

    resuseconfig = ResourceUseDisplay(parent=nbapp)
    nbapp.web_app.settings["trash_display_config"] = resuseconfig

    # This is the ever-shouting promethius loop for values
    callback = ioloop.PeriodicCallback(PrometheusHandler(TrashMetricsLoader(nbapp)), 1000)
    callback.start()
