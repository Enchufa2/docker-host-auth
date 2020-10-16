# from https://github.com/jupyterhub/jupyterhub/issues/1107#issuecomment-302096630
import os
import sys
import pwd
from subprocess import check_output
from jupyterhub.spawner import LocalProcessSpawner, _try_setcwd

def set_user_setuid(username):
    user = pwd.getpwnam(username)
    uid = user.pw_uid
    gid = user.pw_gid
    home = user.pw_dir
    gids = [gid]

    try:
        groupnames = check_output(['groups', username]).split()[2:]
        ents = (check_output(['getent', 'group'] + groupnames)
            .decode('utf-8')
            .split('\n'))
        gids = [int(g.split(':')[2]) for g in ents if g]
        print('Set gids for %s to %s' % (username, gids), file=sys.stderr)
    except Exception as e:
        print('Could not get groups for user: %s' % username, file=sys.stderr)

    def preexec():
        os.setgid(gid)
        try:
            os.setgroups(gids)
            print('User = %s, Gid = %s, gids = %s' % (username, gid, gids), file=sys.stderr)
        except Exception as e:
            print('Failed to set groups for user %s' % username, file=sys.stderr)

        os.setuid(uid)

        _try_setcwd(home)

    return preexec

class MySpawner(LocalProcessSpawner):
    def make_preexec_fn(self, name):
        return set_user_setuid(name)

