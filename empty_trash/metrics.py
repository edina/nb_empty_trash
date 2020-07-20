import os
from pathlib import Path

import psutil
from notebook.notebookapp import NotebookApp


class TrashMetricsLoader:
    def __init__(self, nbapp: NotebookApp):
        self.config = nbapp.web_app.settings["trash_display_config"]
        self.nbapp = nbapp

    def get_trash_size(self):  # , process_metrics, system_metrics):
        root_directory = Path(self.config.trash_dir)
        trash_usage = sum(
            f.stat().st_size for f in root_directory.glob("**/*") if f.is_file()
        )
        return {"trash_usage": trash_usage}

    # Usage is the count of files
    # total is max space on disk
    def disk_metrics(self):
        root_directory = Path(self.config.disk_dir)
        disk_usage = sum(
            f.stat().st_size for f in root_directory.glob("**/*") if f.is_file()
        )
        disk_psutils = psutil.disk_usage(self.config.disk_dir).total
        return {"disk_usage": disk_usage, "disk_total": disk_psutils}
