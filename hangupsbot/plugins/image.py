"""
instructions:
* get CSE Search ID from https://cse.google.co.in/cse/
* put CSE Search ID in config.json:cse
* more info on https://developers.google.com/custom-search/
*
* get image API key from https://console.developers.google.com/apis/
* put image API key in config.json:image-api
"""

import hangups
import plugins
import json
import re, io, os
import html, aiohttp
import urllib.request, urllib.parse

def _initialise(bot):
  plugins.register_user_command(["image"])

def image(bot, event, *args, number=0):
  try:
    int(number)
  except ValueError:
    number = 0
  error = 0
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  cse = bot.get_config_option("cse")
  cse = cse.replace(":","%3A")
  api = bot.get_config_option("image-api")
  url = u'https://www.googleapis.com/customsearch/v1?q=' + query + u'&cx=' + cse + u'&key=' + api
  try:
    search_response = urllib.request.urlopen(url)
  except:
    error = 1
  if error is 0:
    search_results = search_response.read().decode("utf8")
    results = json.loads(search_results)
    try:
      data = results['items'][number]['pagemap']['cse_image'][0]['src']
    except KeyError:
      data = "placeholder"
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
          _("There was some problem with image."))
  else:
    yield from bot.coro_send_message(
        event.conv,
        _("Ran out of today's quota. Try again later."))
