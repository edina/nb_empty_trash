# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import subprocess

from jupyter_core.paths import jupyter_data_dir

c = get_config()
c.NotebookApp.ip = "*"
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False

c.NotebookApp.allow_origin = "*"

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = True


# Change default umask for all subprocesses of the notebook server if set in
# the environment
if "NB_UMASK" in os.environ:
    os.umask(int(os.environ["NB_UMASK"], 8))
