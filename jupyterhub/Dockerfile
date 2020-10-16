FROM jupyterhub/jupyterhub

LABEL maintainer="Iñaki Ucar <iucar@fedoraproject.org>"

RUN apt-get update \
    && apt-get install -y \
        sssd \
        jupyter-notebook \
    && apt-get autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install jupyterlab

# see https://github.com/jupyterhub/jupyterhub/issues/1107
COPY my_spawner.py /usr/lib/python3/dist-packages/
RUN printf "\n\
c.Spawner.default_url = '/lab'\n\
c.JupyterHub.base_url = '/jupyter'\n\
c.PAMAuthenticator.admin_groups = {'wheel'}\n\
c.JupyterHub.spawner_class = 'my_spawner.MySpawner'\n\
" >> jupyterhub_config.py

RUN printf "\n\
auth required pam_sss.so\n\
account required pam_sss.so\n\
password required pam_sss.so\n\
session required pam_sss.so\n\
" > /etc/pam.d/login
