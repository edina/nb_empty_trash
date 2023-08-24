from typing import Optional

from notebook.notebookapp import NotebookApp
from prometheus_client import Gauge

from empty_trash.metrics import TrashMetricsLoader

try:
    # Traitlets >= 4.3.3
    from traitlets import Callable
except ImportError:
    from .utils import Callable


class PrometheusHandler(Callable):
    def __init__(self, metricsloader: TrashMetricsLoader):
        super().__init__()
        self.metricsloader = metricsloader
        self.config = metricsloader.config
        self.session_manager = metricsloader.nbapp.session_manager

        gauge_names = ["total_home", "max_home"]
        for name in gauge_names:
            phrase = name + "_usage"
            gauge = Gauge(phrase, "counter for " + phrase.replace("_", " "), [])
            setattr(self, phrase.upper(), gauge)

    async def __call__(self, *args, **kwargs):

        # two values
        disk_metric_values = self.metricsloader.disk_metrics()
        self.TOTAL_HOME_USAGE.set(disk_metric_values["disk_usage"])
        self.MAX_HOME_USAGE.set(self.apply_disk_limit(disk_metric_values))

    def apply_disk_limit(self, disk_metric_values) -> Optional[str]:
        if disk_metric_values is None:
            return None
        else:
            if callable(self.config.disk_limit):

                return self.config.disk_limit(disk_usage=disk_metric_values["disk_usage"])
            elif self.config.disk_limit > 0:  # disk_limit is an Int
                return self.config.disk_limit
            else:
                return disk_metric_values["disk_total"]
