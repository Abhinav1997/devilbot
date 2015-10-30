import hangups

import plugins

import urllib.request, sys, re, os
from bs4 import BeautifulSoup

def _initialise(bot):
  plugins.register_user_command(["spam"])
    
def spam(bot, event, *args):
  spam = []
  htm = urllib.request.urlopen("http://randomtextgenerator.com").read()
  soup = BeautifulSoup(htm, "html5lib")
  texts = soup.findAll(text=True)
  spam = soup.findAll(attrs={'id' : 'generatedtext'})[0].getText()
  spam = os.linesep.join([s for s in spam.splitlines() if s])
  yield from bot.coro_send_message(
      event.conv,
      _(spam))
