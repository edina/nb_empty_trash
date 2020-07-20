FROM jupyter/minimal-notebook:dc9744740e12

USER root
WORKDIR /srv
# RUN git clone --depth 1 https://github.com/edina/nbresuse
COPY . empty-trash
RUN pip install /srv/empty-trash/ \
    && jupyter nbextension install --sys-prefix --py empty_trash \
    && jupyter nbextension enable empty_trash --py --sys-prefix \
    && jupyter serverextension enable --py empty_trash --sys-prefix
COPY jupyter_notebook_config.py /etc/jupyter/
ENV JUPYTER_CONFIG_DIR /etc/jupyter

USER $NB_USER
WORKDIR $HOME
