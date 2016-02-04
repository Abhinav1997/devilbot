import re, io, os
import html, aiohttp
import urllib.request, urllib.parse
from bs4 import BeautifulSoup

import plugins

def _initialise(bot):
  plugins.register_user_command(["xkcd"])
    
def xkcd(bot, event, *args):
  init_htm = urllib.request.urlopen("http://xkcd.com/archive/").read()
  init_soup = BeautifulSoup(init_htm, "html5lib")
  if ' '.join(args).strip().lower() == "latest":
    htm = urllib.request.urlopen("http://xkcd.com" + init_soup.findAll('a')[10].get('href')).read()
  else:
    htm = urllib.request.urlopen("http://c.xkcd.com/random/comic/").read()
  soup = BeautifulSoup(htm, "html5lib")
  image_link = soup.findAll('img')[1].get('src')
  image_link = "http:" + image_link
  filename = os.path.basename(image_link)
  r = yield from aiohttp.request('get', image_link)
  raw = yield from r.read()
  image_data = io.BytesIO(raw)
  image_id = yield from bot._client.upload_image(image_data, filename=filename)
  yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)
