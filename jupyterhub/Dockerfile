FROM fedora:36
LABEL maintainer="Iñaki Ucar <iucar@fedoraproject.org>"
WORKDIR /srv/jupyterhub/

RUN dnf -y install langpacks-en python3.8 npm sssd-client java-11-openjdk-headless \
  && dnf -y clean all
ENV LANG=en_US.UTF-8
RUN ln -s /usr/bin/python3.8 /usr/local/bin/python3 \
  && ln -s /usr/local/bin/python3 /usr/local/bin/python

RUN python -m ensurepip --upgrade
RUN pip3 install jupyterhub jupyterlab notebook voila
RUN npm install -g configurable-http-proxy

# see https://github.com/jupyterhub/jupyterhub/issues/1107
COPY my_spawner.py /usr/lib/python3.8/site-packages/
RUN printf "\n\
c.Spawner.default_url = '/lab'\n\
c.JupyterHub.base_url = '/jupyter'\n\
c.PAMAuthenticator.admin_groups = {'wheel'}\n\
c.PAMAuthenticator.allow_all = True\n\
c.JupyterHub.spawner_class = 'my_spawner.MySpawner'\n\
" >> jupyterhub_config.py

RUN printf "\n\
auth required pam_sss.so\n\
account required pam_sss.so\n\
password required pam_sss.so\n\
session required pam_sss.so\n\
" > /etc/pam.d/login

CMD ["jupyterhub"]
