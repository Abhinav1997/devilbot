"""
instructions:
* get google API key from https://console.developers.google.com/apis/
* put google API key in config.json:google-api
"""

import hangups
import plugins
import json
import re, io, os
import html, aiohttp
import urllib.request, urllib.parse

def _initialise(bot):
  gapi = bot.get_config_option("google-api")
  if gapi and gapi != "GOOGLE_API_KEY":
    plugins.register_user_command(["youtube"])

def youtube(bot, event, *args):
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  api = bot.get_config_option("google-api")
  url = u'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + query + u'&key=' + api
  search_response = urllib.request.urlopen(url)
  search_results = search_response.read().decode("utf8")
  results = json.loads(search_results)
  try:
    title = results['items'][0]['snippet']['title']
  except IndexError:
    yield from bot.coro_send_message(
        event.conv,
        _("No results found."))
    return
  for i in range (0,4):
    error = 0
    try:
      title = results['items'][i]['snippet']['title']
      data = results['items'][i]['id']['videoId']
    except KeyError:
      error = 1
    if error != 1:
      break
  if error != 1:
    video = "https://www.youtube.com/watch?v=" + data
    yield from bot.coro_send_message(
        event.conv,
        _(title + "<br>" + video))
  else:
    yield from bot.coro_send_message(
        event.conv,
        _("No videos found"))
