import hangups

import plugins

import urllib.request, sys, re, os
from bs4 import BeautifulSoup

def _initialise(bot):
  plugins.register_user_command(["compliment"])
    
def compliment(bot, event, *args):
  name = ' '.join(args).strip().title()
  htm = urllib.request.urlopen("http://www.madsci.org/cgi-bin/cgiwrap/~lynn/jardin/SCG").read()
  soup = BeautifulSoup(htm, "html5lib")
  compli = soup.h2.string
  compli = os.linesep.join([s for s in compli.splitlines() if s])
  if name:
    compli = name + ', ' + compli
  yield from bot.coro_send_message(
      event.conv,
      _(compli))
