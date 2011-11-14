import logging
import os
import re
import string

from pyramid import httpexceptions as http
from pyramid.security import authenticated_userid

from cornice import Service

aliases = Service(name='aliases', path='/alias/',
                  description='Manage the email <=> alias store.')

alias_detail = Service(name='alias-detail', path='/alias/{alias}',
                       description='Manage a single alias.')


logger = logging.getLogger(__file__)

# Not the best; just make sure it looks like x@y.z.
EMAIL_RE = '[^@]+@[^.]+.\w+'


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
    email = authenticated_userid(request)

    if request.body:
        try:
            alias = request.json_body['alias']
        except Exception:
            raise http.HTTPBadRequest()
    else:
        alias = new_alias(domain=request.registry.settings['email_domain'])
    if not re.match(EMAIL_RE, alias) or db.resolve_alias(alias):
        raise http.HTTPBadRequest()

    db.add_alias(email, alias)
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
