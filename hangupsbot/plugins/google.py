"""
instructions:
* get CSE Search ID from https://cse.google.co.in/cse/
* put CSE Search ID in config.json:cse
* more info on https://developers.google.com/custom-search/
*
* get google API key from https://console.developers.google.com/apis/
* put google API key in config.json:google-api
"""

import re, os, io
import html, aiohttp
import json
import urllib.request

import plugins

def _initialise(bot):
  gapi = bot.get_config_option("google-api")
  if gapi:
    plugins.register_user_command(["image", "search", "youtube"])

def search(bot, event, *args):
  error = 0
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  cse = bot.get_config_option("cse")
  cse = cse.replace(":","%3A")
  api = bot.get_config_option("google-api")
  url = u'https://www.googleapis.com/customsearch/v1?q=' + query + u'&cx=' + cse + u'&key=' + api
  try:
    search_response = urllib.request.urlopen(url)
  except:
    error = 1
  if error is 0:
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    title = results['items'][0]['htmlTitle']
    link = results['items'][0]['link']
    desc = results['items'][0]['htmlSnippet']
    yield from bot.coro_send_message(
        event.conv,
        _(title))
    yield from bot.coro_send_message(
        event.conv,
        _(desc))
    yield from bot.coro_send_message(
        event.conv,
        _(link))
  else:
    yield from bot.coro_send_message(
        event.conv,
        _("Ran out of today's quota. Try again later."))

def image(bot, event, *args):
  error = 0
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  if not squery:
    yield from bot.coro_send_message(
        event.conv,
        _("Please provide the detail of image you are looking for."))
    return
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  cse = bot.get_config_option("cse")
  cse = cse.replace(":","%3A")
  api = bot.get_config_option("google-api")
  url = u'https://www.googleapis.com/customsearch/v1?q=' + query + u'&cx=' + cse + u'&key=' + api
  try:
    search_response = urllib.request.urlopen(url)
  except:
    error = 1
  if error is 0:
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    for i in range (0,9):
      try:
        data = results['items'][i]['pagemap']['cse_image'][0]['src']
        if data.endswith((".jpg", ".gif", "gifv", "webm", "png", "jpeg")):
          break
      except KeyError:
        data = "placeholder"
      except IndexError:
        data = "placeholder"
        break
    if data.endswith((".jpg", ".gif", "gifv", "webm", "png", "jpeg")):
      filename = os.path.basename(data)
      r = yield from aiohttp.request('get', data)
      raw = yield from r.read()
      image_data = io.BytesIO(raw)
      image_id = yield from bot._client.upload_image(image_data, filename=filename)
      yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)
    else:
      yield from bot.coro_send_message(
          event.conv,
          _("No suitable images found."))
  else:
    yield from bot.coro_send_message(
        event.conv,
        _("Ran out of today's quota. Try again later."))

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
    except IndexError:
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
