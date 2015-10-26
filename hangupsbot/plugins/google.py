import hangups

import plugins

import json

import re

import html

import urllib.request, urllib.parse

def _initialise(bot):
  plugins.register_user_command(["google"])

def google(bot, event, *args):
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  url = u'http://ajax.googleapis.com/ajax/services/search/web?v=2.0&q=' + query
  search_response = urllib.request.urlopen(url)
  search_results = search_response.read().decode("utf8")
  results = json.loads(search_results)
  data = results['responseData']
  hits = data['results']
  num = 0
  for h in hits:
    while num == 0:
      title = h['title']
      url = h['url']
      num = 1
  url = urllib.request.unquote(url)
  title = html.unescape(title)

  yield from bot.coro_send_message(
      event.conv,
      _(title))
  yield from bot.coro_send_message(
      event.conv,
      _(url))
