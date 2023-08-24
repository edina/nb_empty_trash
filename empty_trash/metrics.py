import os
from pathlib import Path

import psutil
from notebook.notebookapp import NotebookApp


class TrashMetricsLoader:
    def __init__(self, nbapp: NotebookApp):
        self.config = nbapp.web_app.settings["trash_display_config"]
        self.nbapp = nbapp

    # Usage is the count of files
    # total is max space on disk
    def disk_metrics(self):
        disk_psutils = psutil.disk_usage(self.config.disk_dir)
        return {"disk_usage": disk_psutils.used, "disk_total": disk_psutils.total}
