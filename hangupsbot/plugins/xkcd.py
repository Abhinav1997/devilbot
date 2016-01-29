import hangups
import plugins
import re, io, os
import html, aiohttp
import urllib.request, urllib.parse
from bs4 import BeautifulSoup

def _initialise(bot):
  plugins.register_user_command(["xkcd"])
    
def xkcd(bot, event, *args):
  image_link = "//imgs.xkcd.com/comics/xkcd_stack.png"
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
