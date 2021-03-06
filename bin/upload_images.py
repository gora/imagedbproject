# -*- coding: utf-8 -*-
# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os, re
import logging
from optparse import OptionParser
import urllib, urllib2, urlparse, httplib
import MultipartPostHandler

PATH = '.'
USER = 'ciboe'
PASSWORD = 'ciboe'
#URL = 'http://localhost:8000/'
URL = 'http://imagedb.ciboe.dk/'
ADMIN_PATH = '/admin/files/image/add/'
LOGIN_PATH = '/login/'

category_mapping = {
    'A':'locations',
    'a':'locations',
    'B':'fields',
    'b':'fields',
    'C':'installations',
    'c':'installations',
    'D':'people',
    'd':'people',
    'E':'hse',
    'e':'hse',
    'F':'events',
    'f':'events',
    'G':'graphics',
    'g':'graphics',
    'H':'communications',
    'h':'communications',
    'I':'archives',
    'i':'archives',}

# valid file extensions
file_ext = ('.tif', '.TIF', '.jpg', '.JPG', '.jpeg', '.JPEG',)

class MockFileObject(object):
    def read(self):
        return None

    def close(self):
        pass

class MockOpener(object):
    def open(self, *args, **kwargs):
        return MockFileObject()

# count number of uploads
count = 0

def handle_file(opener, dirname, name):

    # find categories
    categories = re.findall(r'[A-Z|a-z][0-9]{2}',dirname)
    image = os.path.join(dirname, name)

    logging.debug('uploading image %s with categories %s...' % (image, categories))

    params = [('is_public', 'on'), ('_save', 'Save'), ("image", open(image, "rb")) ]
    try:
        params += [(category_mapping[category[0]], str(int(category[1:3]))) for category in categories]
    except KeyError:
        logging.debug('failed')
        return

    try:
        f = opener.open(urlparse.urljoin(URL, ADMIN_PATH), params)
        data = f.read()
        f.close()
    except Exception, e:
        logging.debug('failed %s' % e)
        return

def main():
    # options
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="path",
                      help="path to root dir", metavar="PATH")
    parser.add_option("-u", "--user", dest="user",
                      help="username")
    parser.add_option("-p", "--password", dest="password",
                      help="password")
    parser.add_option("-l", "--url", dest="url",
                      help="host url")
    parser.add_option("-f", action="store_true", dest="pretend", default=False,
                      help="pretend image upload")
    parser.add_option("-s", "--skip", dest="skip", type="int",
                      help="skip x images", default=0)

    (options, args) = parser.parse_args()

    path = options.path or PATH
    user = options.user or USER
    password = options.password or PASSWORD
    url = options.url or URL
    pretend = options.pretend
    skip = options.skip

    # init url lib with cookie based auth handler
    if pretend:
        opener = MockOpener()
    else:
        opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(), MultipartPostHandler.MultipartPostHandler)
        urllib2.install_opener(opener)

    # do login
    params = urllib.urlencode(dict(username=user, password=password))
    f = opener.open(urlparse.urljoin(url, LOGIN_PATH), params)
    data = f.read()
    f.close()

    def visit(arg, dirname, names):
        # handle each file
        global count
        for index, name in enumerate(names):
            path = os.path.join(dirname, name)
            if os.path.isfile(path):

                if "Recycled" in path or "System Volume Information" in path:
                    continue

                if name.startswith('.'):
                    print 'dropping %s...' % name
                    continue

                # check for valid file extensions
                base, ext = os.path.splitext(name)
                if ext not in file_ext:
                    print "Invalid file extension for %s%s" % (base, ext)
                    continue

                if count >= skip:
                    handle_file(arg, dirname, name)
                else:
                    print 'skipping %s...' % name
                count += 1

    # walk the dir tree
    os.path.walk(path, visit, opener)

if __name__ == "__main__":
    main()
