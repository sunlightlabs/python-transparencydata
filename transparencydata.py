__author__ = "Jeremy Carbaugh (jcarbaugh@sunlightfoundation.com)"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Sunlight Labs"
__license__ = "BSD"

import sys

if sys.version_info[0] == 3:
    from urllib.parse import urlencode, urljoin
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:    
    from urllib import urlencode
    from urlparse import urljoin
    from urllib2 import HTTPError, urlopen

try:
    import json
except ImportError:
    import simplejson as json

DEFAULT_URL = "http://transparencydata.com/api/1.0/"
DEFAULT_PARAMETERS = ('apikey','page','per_page')
DEFAULT_HANDLERS = {}

class TransparencyDataError(Exception):
    pass

from api import api, DEFAULT_CYCLE

# base client
class Client(object):
    
    def __init__(self, key):
        self.apikey = key
        self.apiurl = DEFAULT_URL
        self.debug = False
        
    def __call__(self, **kwargs):
        
        kwargs['apikey'] = self.apikey
        params = {}
        
        handlers = {}
        handlers.update(DEFAULT_HANDLERS)
        if hasattr(self, 'handlers'):
            handlers.update(self.handlers)
        
        for param, value in kwargs.iteritems():
            
            (name, operator) = param.split('__') if '__' in param else (param, None)
            
            if name not in self.parameters and name not in DEFAULT_PARAMETERS:
                raise TransparencyDataError('%s is not a valid parameter' % param)
            
            if operator == 'in':
                if isinstance(value, (list, tuple)):
                    value = "|".join(str(v) for v in value)
                else:
                    operator = None
            
            elif operator == 'gt':
                value = ">|%s" % value
                
            elif operator == 'lt':
                value = "<|%s" % value
                
            elif operator == 'between':
                if not isinstance(value, (list, tuple)):
                    raise TransparencyDataError('%s__%s must be a tuple or list' % (name, operator))
                start = value[0].strftime("%Y-%m-%d")
                end = value[1].strftime("%Y-%m-%d")
                value = "><|%s|%s" % (start, end)
            
            handler = handlers.get(name, None)
            if handler:
                value = handler(name, value, operator)
            
            params[name] = value.encode('utf8')

        url = "%s?%s" % (urljoin(self.apiurl, self.endpoint), urlencode(params))
        if self.debug:
            print url
            return
        
        try:
            response = urlopen(url).read().decode()
            return json.loads(response)
        except HTTPError, e:
            raise TransparencyDataError(e.read())
        except (ValueError, KeyError), e:
            raise TransparencyDataError('Invalid Response')

# base types
class ContributionsClient(Client):
    endpoint = 'contributions.json'
    parameters = (
        'amount','contributor_ft','contributor_state','cycle',
        'date','employer_ft','recipient_ft','recipient_state',
        'seat','transaction_namespace','contributor_industry',
    )

class LobbyingClient(Client):
    endpoint = 'lobbying.json'
    parameters = (
        'amount','client_ft','client_parent_ft','filing_type',
        'lobbyist_ft','registrant_ft','transaction_id',
        'transaction_type','year'
    )

# main wrapper
class TransparencyData(object):
    
    def __init__(self, key):
        self.contributions = ContributionsClient(key)
        self.lobbying = LobbyingClient(key)
