# Authenticating a docker container against host's Unix accounts

Minimal steps to expose the host's UNIX accounts to docker containers through
the host's [SSSD](https://sssd.io/) daemon, without mounting the `shadow` file,
plus an application to JupyterHub. Inspired by
[this post](https://jhrozek.wordpress.com/2015/03/31/authenticating-a-docker-container-against-hosts-unix-accounts/)
and [this repository](https://github.com/arcenik/docker-authfromhost).

## Host configuration

Modern distributions ship and enable SSSD by default. On Fedora, it is enough
to copy the included configuration file and restart the daemon:

```bash
$ cp /usr/lib64/sssd/conf/sssd.conf /etc/sssd/
$ chmod 0600 /etc/sssd/sssd.conf
$ systemctl restart sssd
```

These are the contents of the configuration file:

```bash
$ cat /etc/sssd/sssd.conf
[sssd]
services = nss, pam
domains = shadowutils

[nss]

[pam]

[domain/shadowutils]
id_provider = files

auth_provider = proxy
proxy_pam_target = sssd-shadowutils

proxy_fast_alias = True
```

which uses the following PAM configuration file:

```bash
$ cat /etc/pam.d/sssd-shadowutils 
#%PAM-1.0
auth        [success=done ignore=ignore default=die] pam_unix.so nullok try_first_pass
auth        required      pam_deny.so

account     required      pam_unix.so
account     required      pam_permit.so
```

## Container configuration

The container requires the SSSD client and a PAM configuration file that diverts
authentication through the `pam_sss.so` module, which talks to the appropriate
socket (which must be mounted, details below).

- The [fedora](https://github.com/Enchufa2/docker-host-auth/tree/master/fedora)
and [debian](https://github.com/Enchufa2/docker-host-auth/tree/master/debian)
directories contain Dockerfiles with these minimum requirements.
- The [jupyterhub](https://github.com/Enchufa2/docker-host-auth/tree/master/jupyterhub)
directory applies this configuration to a JupyterHub image.

## Launch the container

Finally, you just need to bind-mount the host's `/var/lib/sss/pipes` directory,
since the SSSD Unix sockets are located there, and you are ready to go:

```bash
$ docker run <flags> -v /var/lib/sss/pipes:/var/lib/sss/pipes <image>
```

Also, and particularly for the JupyterHub use case, you may want to bind-mount
the `/home` directory too, so that logged users access their home directories.
