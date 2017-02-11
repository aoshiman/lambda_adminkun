# -*- coding: utf-8 -*-

import requests
from twython import Twython, TwythonError
from bs4 import BeautifulSoup
from boto3 import Session
from setting import (CONSUMER_KEY, CONSUMER_SECRET,
                     ACCESS_TOKEN, ACCESS_SECRET,
                     DOMAIN, END_POINT, UA, BUCKET)


def fetch_episodes():
    headers = {'User-Agent': UA}
    response = requests.get(DOMAIN + END_POINT, headers=headers)
    response.encoding = 'SHIFT_JIS'
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    titles = []
    for node in soup.findAll('div', {'id': 'adminkun-new-articles'}):
        for tag in node.findAll('a', href=True):
            links.append(tag['href'])

        for tag in node.findAll('h4'):
            titles.append(tag.string)

    episodes = []
    for (title, link) in zip(titles, links):
        episodes.append([title, link])

    episodes.reverse()
    return episodes


def get_episode_list(bucket):
    s3 = Session().resource('s3')
    bucket = s3.Bucket(bucket)
    return [obj.key for obj in bucket.objects.all()]


def put_episode(bucket, keyname):
    s3 = Session().resource('s3')
    bucket = s3.Bucket(bucket)
    obj = bucket.Object(keyname)
    body = keyname
    response = obj.put(
            Body=body.encode('utf-8'),
            ContentEncoding='utf-8',
            ContentType='text/plane'
            )


def tweet_episode():
    """OAuth setting and Twit(if episode is new)"""
    twitter = Twython(
                      CONSUMER_KEY,
                      CONSUMER_SECRET,
                      ACCESS_TOKEN,
                      ACCESS_SECRET
                      )
    try:
        lists = get_episode_list(BUCKET)
    except:
        pass

    episodes = fetch_episodes()
    for episode in episodes:
        url, title = episode[1], episode[0]
        _eps_id = url.split('/')
        eps_id = _eps_id[7]
        if not eps_id in lists:
            post = u'{0} {1}'.format(title, url)
            try:
                #  twitter.update_status(status=post)
                print(post)
            except TwythonError as e:
                print(e)
            finally:
                put_episode(BUCKET, eps_id)


def lambda_handler(event, context):
    tweet_episode()


if __name__ == '__main__':
    tweet_episode()

