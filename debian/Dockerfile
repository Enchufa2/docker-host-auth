FROM debian:latest

LABEL maintainer="Iñaki Ucar <iucar@fedoraproject.org>"

RUN apt-get update && apt-get install -y sssd

RUN printf "\n\
auth required pam_sss.so\n\
account required pam_sss.so\n\
password required pam_sss.so\n\
session required pam_sss.so\n\
" > /etc/pam.d/login
