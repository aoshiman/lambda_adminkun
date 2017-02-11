## -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import yaml
import lamvery

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 \
                    (KHTML, like Gecko) Version/6.0 Mobile/10A403 Safari/8536.25"
DOMAIN = 'http://www.atmarkit.co.jp'
END_POINT = '/ait/subtop/features/windows/adminkun_index.html'
BUCKET = 'adminkun.aoshiman.org'

try:
    with open(lamvery.secret.file('config.yml')) as f:
    #  with open('config.yml') as f:
        _oauth_conf = yaml.load(f)

except Exception as e:
    print(e)

CONSUMER_KEY = _oauth_conf['consumer_key']
CONSUMER_SECRET = _oauth_conf['consumer_secret']
ACCESS_TOKEN = _oauth_conf['access_token']
ACCESS_SECRET = _oauth_conf['access_secret']
