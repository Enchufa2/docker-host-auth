FROM fedora:latest

LABEL maintainer="Iñaki Ucar <iucar@fedoraproject.org>"

RUN dnf install -y sssd-client

RUN printf "\n\
auth required pam_sss.so\n\
account required pam_sss.so\n\
password required pam_sss.so\n\
session required pam_sss.so\n\
" > /etc/pam.d/login
