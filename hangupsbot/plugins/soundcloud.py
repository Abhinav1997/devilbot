"""
instructions:
* get soundcloud API key from https://developers.soundcloud.com/
* put soundcloud API key in config.json:soundcloud-api
"""

import json
import re
import urllib.request

import plugins

def _initialise(bot):
  sapi = bot.get_config_option("soundcloud-api")
  if sapi and sapi != "SOUNDCLOUD_API_KEY":
    plugins.register_user_command(["soundcloud"])

def soundcloud(bot, event, *args):
  squery = ' '.join(args).strip()
  squery = squery.replace(" ", "+")
  query = re.sub(r'^\.g', u'', squery, re.UNICODE).encode('utf-8')
  query = query.strip()
  query = urllib.request.quote(query)
  api = bot.get_config_option("soundcloud-api")
  url = u'http://api.soundcloud.com/tracks?q=' + query + u'&client_id=' + api
  search_response = urllib.request.urlopen(url)
  search_results = search_response.read().decode("utf8")
  results = json.loads(search_results)
  try:
    title = results[0]['title']
  except IndexError:
    yield from bot.coro_send_message(
        event.conv,
        _("No results found."))
    return
  song = results[0]['permalink_url']  
  yield from bot.coro_send_message(
      event.conv,
      _(title + "<br>" + song))
