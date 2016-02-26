#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'Lukas Schauer'
AUTHOR_NICK = 'lukas2511'
AUTHOR_LOCATION = 'Bonn, Germany'
AUTHOR_IMAGE = 'https://www.gravatar.com/avatar/38df18cf53121c48865d1edadc393069?s=200&amp;d=mm&amp;r=x'
AUTHOR_DESCRIPTION = 'Hey! I&#x27;m Lukas and I&#x27;m currently studying computer science at Hochschule Bonn-Rhein-Sieg and I&#x27;m working as Linux system administrator. As a hobby I like to play with electronics and embedded systems.</p>'

AUTHOR_SAVE_AS = 'author/' + AUTHOR_NICK + '/index.html'
AUTHOR_TWITTER = AUTHOR_NICK
AUTHOR_GITHUB = AUTHOR_NICK

SITENAME = 'lukas.im'
SITEURL = os.getenv('SITEURL') if os.getenv('SITEURL') else 'http://localhost:8000'

THEME = 'theme'

PATH = 'content'
STATIC_PATHS = ['blog']
ARTICLE_PATHS = ['blog']
ARTICLE_SAVE_AS = '{date:%Y/%m/%d}/{slug}/index.html'
ARTICLE_URL = '{date:%Y/%m/%d}/{slug}/index.html'
PAGE_SAVE_AS = '{slug}.html'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'atom.xml'
FEED_ALL_RSS = 'rss.xml'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'en'

PLUGINS = ['advthumbnailer', 'autostatic', 'plugins.summary']

# Feed generation is usually not desired when developing
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Date format
DEFAULT_DATE_FORMAT = '%d %B %Y'

# Navigation
NAVIGATION = (('Home', SITEURL),
              ('Projects', SITEURL + '/category/projects/'),
              ('Archives', SITEURL + '/archives.html'))

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
