S3 Static
=========

Want an A grade on the Y!Slow test? Ship your website assets with this script!

Features
--------

+ Gzips text based files over 1kb
+ Content-Type set from filename extension
+ Far future Expires and Cache-Control
+ Familiar rsync behavior with trailing slashes
+ Resulting URI to stdout is the only output
+ No messing around with stupid compiling CoffeeScript, Stylus, concatenating
  files or minifying JavaScript. This is the job of a frontend compiler (see
  Brunch or Yeoman).

Install
-------

    $ pip install ssstatic

Usage
-----

Dry run:

    $ DRYRUN=true ssstatic static/ my-bucket/static/

Upload:

    $ export AWS_ACCESS_KEY_ID ...
    $ export AWS_SECRET_ACCESS_KEY ...
    $ ssstatic static/ my-bucket/static/

With cachebusting:

    $ ssstatic -c static/ my-bucket/static/  # uploads to something like //my-bucket.s3.amazonaws.com/static/39fj3923/

Site Integration
----------------

I have a Makefile with this command to publish assets and update a Heroku config

    upload:
      heroku config:add STATIC_URL=`honcho run ssstatic app/static/ $(BUCKET)/web/`

A protocol relative URL is the only stdout, so it can be used as a STATIC_URL in
Django for example.
