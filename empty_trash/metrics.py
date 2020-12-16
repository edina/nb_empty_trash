import os
from pathlib import Path

import psutil
from notebook.notebookapp import NotebookApp


class TrashMetricsLoader:
    def __init__(self, nbapp: NotebookApp):
        self.config = nbapp.web_app.settings["trash_display_config"]
        self.nbapp = nbapp

    def get_trash_size(self):
        root_directory = Path(self.config.trash_dir)
        trash_usage = 0
        # trash_usage =sum(
        #     f.stat().st_size for f in root_directory.glob("**/*") if f.is_file()
        # )
        return {"trash_usage": trash_usage}

    # Usage is the count of files
    # total is max space on disk
    def disk_metrics(self):
        disk_psutils = psutil.disk_usage(self.config.disk_dir)
        return {"disk_usage": disk_psutils.used, "disk_total": disk_psutils.total}
