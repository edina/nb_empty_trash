FROM jupyter/minimal-notebook:dc9744740e12

USER root
RUN pip install git+git://github.com/edina/nb_empty_trash.git#egg=nb_empty_trash
# WORKDIR /srv
# COPY . empty-trash
# RUN pip install /srv/empty-trash/
RUN jupyter nbextension install --sys-prefix --py empty_trash \
    && jupyter nbextension enable empty_trash --py --sys-prefix \
    && jupyter serverextension enable --py empty_trash --sys-prefix

# Enable delete-to-trash
COPY jupyter_notebook_config.py /etc/jupyter/
ENV JUPYTER_CONFIG_DIR /etc/jupyter

USER $NB_USER
WORKDIR $HOME
