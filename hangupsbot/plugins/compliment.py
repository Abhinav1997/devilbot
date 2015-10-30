import hangups

import plugins

import urllib.request, sys, re, os
from bs4 import BeautifulSoup

def _initialise(bot):
  plugins.register_user_command(["compliment"])
    
def compliment(bot, event, *args):
  name = ' '.join(args).strip().title()
  compli = []
  htm = urllib.request.urlopen("http://toykeeper.net/programs/mad/compliments").read()
  soup = BeautifulSoup(htm)
  texts = soup.findAll(text=True)
  compli = soup.findAll(attrs={'class' : 'blurb_title_1'})[0].getText()
  compli = os.linesep.join([s for s in compli.splitlines() if s])
  if name:
    compli = name + ', ' + compli
  yield from bot.coro_send_message(
      event.conv,
      _(compli))
