from charms.reactive import when_not
from charms.reactive import set_state
from charmhelpers.core import hookenv
from charmhelpers.fetch import apt_install
import jujuresources


@when_not('bootstrapped')
def bootstrap():
    hookenv.status_set('maintenance', 'Installing base resources')
    apt_install(['python-pip'])
    mirror_url = hookenv.config('resources_mirror')
    if not jujuresources.fetch(mirror_url=mirror_url):
        missing = jujuresources.invalid()
        hookenv.status_set('blocked', 'Unable to fetch required resource%s: %s' % (
            's' if len(missing) > 1 else '',
            ', '.join(missing),
        ))
        return
    jujuresources.install(['pathlib', 'jujubigdata'])
    set_state('bootstrapped')
