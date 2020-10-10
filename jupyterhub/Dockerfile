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

RUN printf "\n\
c.Spawner.default_url = '/lab'\n\
c.JupyterHub.base_url = '/jupyter'\n\
c.PAMAuthenticator.admin_groups = {'wheel'}\n\
" > jupyterhub_config.py

RUN printf "\n\
auth required pam_sss.so\n\
account required pam_sss.so\n\
password required pam_sss.so\n\
session required pam_sss.so\n\
" > /etc/pam.d/login
