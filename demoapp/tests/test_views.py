import unittest2

import mock
from pyramid import testing
from nose.tools import eq_

from demoapp.storage import mem
from demoapp import views


class ViewTest(unittest2.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.email = 'email@foo.com'
        self.config.testing_securitypolicy(userid=self.email, permissive=True)
        self.request = testing.DummyRequest()
        self.request.registry['storage'] = mem.Storage()
        self.request.registry['email_domain'] = 'browserid.org'

    def tearDown(self):
        testing.tearDown()

    def test_add_alias(self):
        response = views.add_alias(self.request)
        eq_(set(response.keys()), set(['email', 'alias']))
        eq_(response['email'], self.email)

    def test_get_alias(self):
        alias = views.add_alias(self.request)['alias']
        self.request.matchdict = {'alias': alias}
        response = views.get_alias(self.request)
        eq_(response, {'email': self.email, 'alias': alias})

    def test_list_aliases(self):
        alias1 = views.add_alias(self.request)['alias']
        alias2 = views.add_alias(self.request)['alias']
        response = views.list_aliases(self.request)
        eq_(response, {'email': self.email, 'aliases': [alias1, alias2]})

    def test_delete_alias(self):
        alias = views.add_alias(self.request)['alias']
        self.request.matchdict = {'alias': alias}
        response = views.delete_alias(self.request)
        eq_(response, {'email': self.email, 'alias': alias})

        self.request.matchdict = None
        eq_(views.list_aliases(self.request),
            {'email': self.email, 'aliases': []})


@mock.patch('demoapp.views.os.urandom')
def test_new_alias(urandom_mock):
    urandom_mock.return_value = ''.join(map(chr, [0, 1, 61, 62, 63, 64]))
    eq_(views.new_alias(), '01Z012@browserid.org')
    eq_(views.new_alias(domain='woo.com'), '01Z012@woo.com')
