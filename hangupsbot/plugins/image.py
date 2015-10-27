import hangups

import plugins

import json

import re, io, os

import html, aiohttp

import urllib.request, urllib.parse

def _initialise(bot):
  plugins.register_user_command(["image"])

def image(bot, event, *args):
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  url = u'http://ajax.googleapis.com/ajax/services/search/images?v=2.0&q=' + query
  search_response = urllib.request.urlopen(url)
  search_results = search_response.read().decode("utf8")
  results = json.loads(search_results)
  data = results['responseData']
  hits = data['results']
  num = 0
  for h in hits:
    title = h['title']
    if h['url'].endswith((".jpg", ".gif", "gifv", "png")):
      while num == 0:
        url = h['url']
        num = 1
  url = urllib.request.unquote(url)

  try:
    title
  except UnboundLocalError:
    yield from bot.coro_send_message(
        event.conv,
        _("No results found."))
  else:
    title = html.unescape(title)
    if url.endswith((".jpg", ".gif", "gifv", "png")):
      filename = os.path.basename(url)
      r = yield from aiohttp.request('get', url)
      raw = yield from r.read()
      image_data = io.BytesIO(raw)
      try:
        image_id = yield from bot._client.upload_image(image_data, filename=filename)
      except KeyError:
        yield from bot.coro_send_message(
            event.conv,
            _("Can't find an image file"))
        return
      yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)
    else:
      yield from bot.coro_send_message(
          event.conv,
          _("Can't find an image file"))
