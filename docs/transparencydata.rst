Transparency Data API
=====================

Usage
=====


The TransparencyData class is constructed with your API key as an initialization parameter:

	>>> from transparencydata import TransparencyData
	>>> td = TransparencyData(<your-api-key>)

If you do not have an API key visit http://services.sunlightlabs.com/api/ to
register for one.

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

Parameter documentation: http://transparencydata.com/api/contributions

Response documentation: http://transparencydata.com/docs/contributions

--------
Lobbying
--------

To find all lobbying conducted by John Wonderlich:

	>>> td.lobbying(lobbyist_ft='john wonderlich')

A list of valid lobbying parameters can be accessed programmatically:

	>>> print td.lobbying.parameters

Parameter documentation: http://transparencydata.com/api/lobbying

Response documentation: http://transparencydata.com/docs/lobbying


--------
Earmarks
--------

To find all earmarks directed towards Seattle, WA:

    >>> td.earmarks(city='Seattle', state='WA')
    
A list of valid earmark parameters can be accessed programmatically:

    >>> print td.earmarks.parameters

Parameter documentation: http://transparencydata.com/api/earmarks

Response documentation: http://transparencydata.com/docs/earmarks


--------------
Federal Grants
--------------

To find all grants made by the NEA in 2010:

    >>> td.grants(agency_ft='national endowment for the arts', fiscal_year='2010')
    
A list of valid grant parameters can be accessed programmatically:

    >>> td.grants.parameters
    
Parameter documentation: http://transparencydata.com/api/grants/

Response documentation: http://transparencydata.com/docs/grants/


-----------------
Federal Contracts
-----------------

To find all federal contracts issued to Bank of America:

    >>> td.contracts(vendor_name='bank of america')
    
A list of valid contract parameters can be accessed programmatically:

    >>> td.contracts.parameters

Parameter documentation: http://transparencydata.com/api/contracts

Response documentation: http://transparencydata.com/docs/contracts


