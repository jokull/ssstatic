#!/usr/bin/env python
# encoding=utf-8

import sys
import datetime
import email
import mimetypes
import os
import time
import gzip
import subprocess
import argparse

from cStringIO import StringIO

from boto.s3.connection import S3Connection


class MD5ExecutableNotFound(Exception):
    pass


def which_md5():
    system_paths = os.environ.get('PATH') or []
    executables = ['md5', 'md5sum']
    for path in system_paths.split(':'):
        for md5 in executables:
            if os.path.exists('{}/{}'.format(path, md5)):
                return md5
    raise MD5ExecutableNotFound


s3 = S3Connection()

GZIP_CONTENT_TYPES = (
    'text/css',
    'application/javascript',
)

GZIP_SIZE_MIN = 1024  # Per recommendation

EXCLUDE_FILENAMES = ('.DS_Store', '.git')

HEADERS = {
    # HTTP/1.0
    'Expires': '%s GMT' % (email.Utils.formatdate(
        time.mktime((datetime.datetime.now() +
            datetime.timedelta(days=365 * 2)).timetuple()))),
    # HTTP/1.1
    'Cache-Control': 'max-age %d' % (3600 * 24 * 365 * 2),
}


def stdout(bucket_name, target_root):
    override_hostname = os.environ.get('STATIC_HOST')
    if override_hostname is not None:
        print "//{host}/{root}/".format(host=override_hostname, root=target_root)
    else:
        print "//{bucket}.s3.amazonaws.com/{root}/".format(
            bucket=bucket_name,
            root=target_root,
        )


def main(media_root, bucket_root, cachebuster=False, stdout=stdout):

    if not os.path.exists(media_root):
        sys.exit(u"Error: Sync path does not exist")

    if '/' in bucket_root:
        bucket_name, prefix = bucket_root.split("/", 1)
    else:
        bucket_name, prefix = bucket_root, ''

    bucket = s3.get_bucket(bucket_name)

    if cachebuster:
        media_root_md5, stderr = (subprocess.
            Popen('tar c %s | %s' % (media_root, which_md5()), stdout=subprocess.PIPE, shell=True).
            communicate())
        if stderr:
            raise Exception(u'Could not get unique folder checksum')

        target_root = os.path.join(
            prefix,
            media_root_md5[:6],  # Only use first 6 letters
        )

    else:
        target_root = prefix

    if not media_root.endswith("/"):
        # We want to copy folder as a whole, not just contents - like rsync
        target_root = os.path.join(target_root, media_root)

    target_root = target_root.rstrip("/")  # Normalize
    stdout(bucket_name, target_root)

    if cachebuster and len(list(bucket.list(prefix=target_root))) > 0:
        return  # No need to upload, this exists

    for root, dirs, files in os.walk(media_root):
        for filename in files:
            if [s for s in EXCLUDE_FILENAMES if root.endswith(s)]:
                continue  # example .git
            if filename in EXCLUDE_FILENAMES:
                continue  # example .DS_Store

            path = os.path.join(root, filename)
            s3_path = os.path.join(os.path.relpath(root, media_root), filename)
            s3_path = os.path.normpath(os.path.join(target_root, s3_path))

            content_type, _ = mimetypes.guess_type(s3_path)
            byte_length = os.stat(path).st_size
            headers = HEADERS.copy()
            key = bucket.new_key(s3_path)

            with file(path) as fp:

                if content_type in GZIP_CONTENT_TYPES and byte_length > GZIP_SIZE_MIN:
                    headers['Content-Encoding'] = 'gzip'
                    compressed = StringIO()
                    with gzip.GzipFile(fileobj=compressed, mode='wr', compresslevel=9) as gzip_fp:
                        gzip_fp.write(fp.read())
                    contents = compressed.getvalue()

                else:
                    contents = fp.read()

            if content_type:
                headers['Content-Type'] = content_type

            if os.environ.get('DRYRUN') == "true":
                for key, value in headers.items():
                    print "%s: %s" % (key, value)
                print s3_path
                print

            else:
                key.set_contents_from_string(
                    contents, headers, replace=True, policy='public-read')


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Upload folder to S3.')
        parser.add_argument(
            '-c', '--cachebuster', action='store_true',
            help="Calculate unique checksum for source contents and upload "
                 "under a unique folder path."
        )
        parser.add_argument('source', help="Path to source directory.")
        parser.add_argument('destination', help="Bucket name and path. Ex: s3.python.org/static")
        args = parser.parse_args()
        main(args.source, args.destination, cachebuster=args.cachebuster)
    except KeyboardInterrupt:
        sys.exit(u"Early exit")
