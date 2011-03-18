"""
The transparencydata module provides API wrappers for the data found on
transparencydata.com.
"""

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


# base client
class Client(object):
    
    def __init__(self, key, base_url=DEFAULT_URL):
        self.apikey = key
        self.apiurl = base_url
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
        'contributor_state',
        'recipient_state',
        'cycle',
        'for_against',
        'contributor_industry',
        'seat',
        'transaction_namespace',
        'transaction_type',
        'contributor_ext_id',
        'recipient_ext_id',
        'organization_ext_id',
        'parent_organization_ext_id',
        'committee_ext_id',
        'contributor_type',
        'recipient_type',
        'date',
        'amount',
        'committee_ft',
        'contributor_ft',
        'employer_ft',
        'organization_ft',
        'recipient_ft',
    )

class LobbyingClient(Client):
    endpoint = 'lobbying.json'
    parameters = (
        'lobbyist_is_rep',
        'industry',
        'transaction_id',
        'transaction_type',
        'filing_type',
        'year',
        'issue',
        'client_ext_id',
        'lobbyist_ext_id', 
        'candidate_ext_id',
        'client_ft',
        'client_parent_ft', 
        'lobbyist_ft',
        'registrant_ft',
        'issue_ft',
    )

class EarmarkClient(Client):
    endpoint = 'earmarks.json'
    parameters = (
        'year',
        'state',
        'member_party',
        'member_state',
        'bill',
        'description',
        'city',
        'member',
        'recipient', 
    )
    

class GrantsClient(Client):
    endpoint = 'grants.json'
    parameters = (
        'assistance_type',
        'fiscal_year',
        'recipient_state', 
        'recipient_type',
        'agency_ft',
        'recipient_ft',
    )
    

class ContractsClient(Client):
    endpoint = 'contracts.json'
    parameters = (
        'agency_id',
        'contracting_agency_id',
        'fiscal_year',
        'place_distrct',
        'place_state',
        'requesting_agency_id',
        'vendor_state',
        'vendor_zipcode',
        'vendor_district',
        'vendor_duns',
        'vendor_parent_duns',
        'agency_name',
        'contracting_agency_name',
        'requesting_agency_name',
        'vendor_name',
        'vendor_city',
        'obligated_amount',
        'current_amount',
        'maximum_amount',    
    )
    

# main wrapper
class TransparencyData(object):
    
    def __init__(self, key):
        self.contributions = ContributionsClient(key)
        self.lobbying = LobbyingClient(key)
        self.earmarks = EarmarkClient(key)
        self.grants = GrantsClient(key)
        self.contracts = ContractsClient(key)
