#!/usr/bin/python3
# Copyright (c) 2020, Fredrik Svensson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import errno
import re
from dateutil import parser

def application (environ, start_response):
    print('{} {}'.format(environ['REQUEST_METHOD'], environ['PATH_INFO']))
    basedir = environ['DOCUMENT_ROOT'] + '/data'
    try:
        os.makedirs(basedir + os.path.dirname(environ['PATH_INFO']))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    response_body = ''
    filename = basedir + environ['PATH_INFO']

    if environ['REQUEST_METHOD'] == 'PUT':
        output = open(filename, 'wb')
        try:
            buf = environ['wsgi.input'].read()
        except IOError as e:
            print(e)
        else:
            if filename[-4:] == '.mpd':
                # Change type static to dynamic to make it playable.
                buf = re.sub('type="dynamic"', 'type="static"', buf)

                # Extract start time and publish time.
                p = re.compile('availabilityStartTime="([^"]*)".*publishTime="([^"]*)"', re.DOTALL)
                m = p.search(buf)
                if (m):
                    # Calculate duration.
                    diff = parser.parse(m.group(2)) - parser.parse(m.group(1))
                    hours, rem = divmod(diff.seconds, 3600)
                    minutes, seconds = divmod(rem, 60)
                    duration = 'PT{}H{}M{}.{}S'.format(hours, minutes, seconds, diff.microseconds)

                    # Insert duration at the end of the MDP header.
                    buf = re.sub(r'(<MPD [^>]*)>', r'\1\n\tmediaPresentationDuration="{}">'.format(duration), buf, 1, re.DOTALL)

            output.write(buf)
            output.close()
            response_body = 'Wrote {}\n\r'.format(filename)
    elif environ['REQUEST_METHOD'] == 'DELETE':
        # Ignore delete.
        pass

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]
