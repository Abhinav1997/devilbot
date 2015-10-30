import hangups

import plugins

import urllib.request, sys, re, os
from bs4 import BeautifulSoup

def _initialise(bot):
  plugins.register_user_command(["insult"])
    
def insult(bot, event, *args):
  name = ' '.join(args).strip().title()
  insult = []
  htm = urllib.request.urlopen("http://randominsults.net").read()
  soup = BeautifulSoup(htm, "html5lib")
  texts = soup.findAll(text=True)
  insult = soup.findAll(attrs={'bordercolor' : '#FFFFFF'})[0].getText()
  insult = os.linesep.join([s for s in insult.splitlines() if s])
  if name:
    insult = name + ', ' + insult
  yield from bot.coro_send_message(
      event.conv,
      _(insult))
