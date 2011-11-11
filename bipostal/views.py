import logging
import os
import string

from pyramid.security import authenticated_userid
from pyramid.view import view_config

from cornice import Service

aliases = Service(name='aliases', path='/alias/',
                  description='Manage the email <=> alias store.')

alias_detail = Service(name='alias-detail', path='/alias/{alias}',
                       description='Manage a single alias.')


logger = logging.getLogger(__file__)


def new_alias(length=64, domain='browserid.org'):
    chars = string.digits + string.letters
    base = len(chars)
    token = ''.join(chars[ord(x) % base] for x in os.urandom(length))
    return '%s@%s' % (token, domain)


@aliases.get(permission='authenticated')
def list_aliases(request):
    db = request.registry['storage']
    email = authenticated_userid(request)
    aliases = db.get_aliases(email) or []
    return {'email': email, 'aliases': aliases}


@aliases.post(permission='authenticated')
def add_alias(request):
    db = request.registry['storage']
    domain = request.registry.settings['email_domain']
    email = authenticated_userid(request)
    alias = db.add_alias(email, new_alias(domain=domain))
    logger.info('New alias for %s.', email)
    return {'email': email, 'alias': alias}


@alias_detail.get()
def get_alias(request):
    """Get the real address for a given alias."""
    db = request.registry['storage']
    alias = request.matchdict['alias']
    email = db.resolve_alias(alias)
    return {'email': email, 'alias': alias}


@alias_detail.delete(permission='authenticated')
def delete_alias(request):
    """Delete an alias."""
    email = authenticated_userid(request)
    db = request.registry['storage']
    alias = request.matchdict['alias']
    db.delete_alias(email, alias)
    logger.info('Deleting alias for %s.', email)
    return {'email': email, 'alias': alias}
