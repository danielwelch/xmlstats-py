Changelog
=========

0.1.4 (2015-11-02)
------------------

Fixes:

- Fixed format_result bug that prevented higher level API functions from working.

Testing:

- Added some basic tests, with Travis CI integration

Documentation:

- Added Travis CI embedded status image to README


0.1.3 (2015-11-02)
------------------

Fixes:

- Fixed bugs in http_get handling of 429 response from xmlstats API server. http_get now waits for the amount of time specified by server 429 response before continuing to make requests.