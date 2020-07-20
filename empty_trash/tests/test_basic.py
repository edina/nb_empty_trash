from mock import MagicMock
from mock import patch

from ..config import ResourceUseDisplay
from ..metrics import TrashMetricsLoader
from ..prometheus import PrometheusHandler


class TestBasic:
    """Some basic tests, checking import, making sure APIs remain consistent, etc"""

    def test_import_serverextension(self):
        """Check that serverextension hooks are available"""
        from empty_trash import (
            _jupyter_server_extension_paths,
            _jupyter_nbextension_paths,
            load_jupyter_server_extension,
        )

        assert _jupyter_server_extension_paths() == [{"module": "empty_trash"}]
        assert _jupyter_nbextension_paths() == [
            {
                "section": "tree",
                "dest": "empty_trash",
                "src": "static",
                "require": "empty_trash/trash",
            }
        ]

    ### OK, parked for now - how do I mock "nbapp.web_app.settings['base_url']"
    # def test_mocks(self):
    #     from empty_trash import (
    #         _jupyter_server_extension_paths,
    #         _jupyter_nbextension_paths,
    #         load_jupyter_server_extension,
    #     )

    #     # mock a notebook app
    #     nbapp_mock = MagicMock()
    #     nbapp_mock.web_app.settings = {}

    #     # mock these out for unit test
    #     with patch("tornado.ioloop.PeriodicCallback") as periodic_callback_mock, patch(
    #         "empty_trash.ResourceUseDisplay"
    #     ) as resource_use_display_mock, patch(
    #         "empty_trash.PrometheusHandler"
    #     ) as prometheus_handler_mock:

    #         # load up with mock
    #         load_jupyter_server_extension(nbapp_mock)

    #         # assert that we installed the application in settings
    #         print(nbapp_mock.web_app.settings)
    #         assert "trash_display_config" in nbapp_mock.web_app.settings

    #         # assert that we instantiated a periodic callback with the fake
    #         # prometheus
    #         assert periodic_callback_mock.return_value.start.call_count == 1
    #         assert prometheus_handler_mock.call_count == 1
    #         # prometheus_handler_mock.assert_called_with(nbapp_mock)

    # It really wants tests for it's config & that it gets stats in sensible paces
    # ... but my brain is failing on this :(
