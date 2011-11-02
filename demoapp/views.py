import uuid

from pyramid.security import authenticated_userid
from pyramid.view import view_config

from cornice import Service

aliases = Service(name='aliases', path='/alias/',
                  description='Manage the email <=> alias store.')


def new_alias():
    # TODO: get the domain from the config.
    return '%s@%s' % (uuid.uuid4().hex, 'browserid.org')


@view_config(route_name='get_address', renderer='simplejson')
def get_address(request):
    """Get the real address for a given alias."""
    db = request.registry['storage']
    email = db.resolve_alias(request.matchdict['alias'])
    return {'email': email}


@aliases.get(permission='authenticated')
def list_aliases(request):
    db = request.registry['storage']
    email = authenticated_userid(request)
    aliases = db.get_aliases(email) or []
    return {'email': email, 'aliases': aliases}


@aliases.post(permission='authenticated')
def add_alias(request):
    db = request.registry['storage']
    email = authenticated_userid(request)
    alias = db.add_alias(email, new_alias())
    return {'email': email, 'alias': alias}
