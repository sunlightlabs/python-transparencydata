=======================
python-transparencydata
=======================

Python library for interacting with the TransparencyData.com API.

The TransparencyData.com API provides campaign contribution and lobbying data.

http://transparencydata.com/api/

python-transparencydata is a project of Sunlight Labs (c) 2010
Written by Jeremy Carbaugh <jcarbaugh@sunlightfoundation.com>

All code is under a BSD-style license, see LICENSE for details.

Source: http://github.com/sunlightlabs/python-transparencydata/

Requirements
============

python >= 2.4

simplejson >= 1.8 (not required with Python 2.6, will use built-in ``json`` module)

Usage
=====

To initialize the api, all that is required is for it to be imported and for an
API key to be defined.

(If you do not have an API key visit http://services.sunlightlabs.com/api/ to
register for one.)

Import TransparencyData class and set your API key:

	>>> from transparencydata import TransparencyData
	>>> td = TransparencyData('sunlight-api-key')

-------------------
Parameter Operators
-------------------

Some parameters allow multiple values or greater than, less than, or between operations. We allow operators to be added similar to the method used by the Django ORM. The operator is appended to the end of the parameter name using double underscore.

	>>> td.contributions(amount=100)			# contributions equal to 100 dollars
	>>> td.contributions(amount__lt=100)		# contributions less than 100 dollars
	
	>>> td.contributions(cycle=1990)			# contributions from the 1990 election cycle
	>>> td.contributions(cycle__in=(1990,2008)) # contributions from the 1990 and 2008 election cycles

gt
	Greater than specified value.

lt
	Less than specified value.

between
	Between the lesser value and greater value. Parameters must be passed as a two-value tuple or list.
	
		>>> td.contributions(date__between=(start_date, end_date))

in
	Matches any in a range of values. Parameter must be a tuple or list.


See the parameter documentation (http://transparencydata.com/api/) to find out which operators are valid for each parameter.

----------------------
Campaign Contributions
----------------------

To find all contributions to Chris Van Hollen from the state of CA during the 2008 election cycle:

	>>> td.contributions(cycle=2008, contributor_state='CA', recipient_ft='van hollen')

A list of valid contributions parameters can be accessed programmatically:

	>>> print td.contributions.parameters

Parameter documentation: http://transparencydata.com/api/#contributions

Response documentation: http://transparencydata.com/docs/#contributions

--------
Lobbying
--------

To find all lobbying conducted by John Wonderlich:

	>>> td.lobbying(lobbyist_ft='john wonderlich')

A list of valid lobbying parameters can be accessed programmatically:

	>>> print td.lobbying.parameters

Parameter documentation: http://transparencydata.com/api/#lobbying

Response documentation: http://transparencydata.com/docs/#lobbying