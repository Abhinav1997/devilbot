"""
instructions:
* get CSE Search ID from https://cse.google.co.in/cse/
* put CSE Search ID in config.json:cse
* more info on https://developers.google.com/custom-search/
*
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
    plugins.register_user_command(["image"])

def image(bot, event, *args):
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
