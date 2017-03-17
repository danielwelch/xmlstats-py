Changelog
=========

1.0.0 (2017-03-17)
------------------

- Complete overhaul of the way data is returned and represented when using this library. Data is now returned as NamedTuples, rather than as either simple dictionaries/lists or "objectified" data as in previous versions.
- Methods were reimplimented to match the endpoints of the xmlstats API. Each method exposed by the XmlStats class corresponds to a single endpoint provided by the API, and accepts the same arguments and parameters. This means users of this library can essentially refer to the already existing xmlstats API documentation.


0.1.5 (2015-11-03)
------------------

Fixes:

- Fixed http_get bug that prevented including paramaters in the next request after a 429 response code from xlmstats server.


0.1.4 (2015-11-02)
------------------

Fixes:

- Fixed format_result bug that prevented higher level API functions from working.

Testing:

- Added some basic tests, with Travis CI integration

Documentation:

- Added Travis CI embedded status image to READMEg


0.1.3 (2015-11-02)
------------------

Fixes:

- Fixed bugs in http_get handling of 429 response from xmlstats API server. http_get now waits for the amount of time specified by server 429 response before continuing to make requests.
