import sys, re, os, random
import urllib.request
from random import randint
from bs4 import BeautifulSoup

import plugins

def _initialise(bot):
  plugins.register_user_command(["compliment", "insult"])

def compliment(bot, event, *args):
  name = ' '.join(args).strip().title()
  htm = urllib.request.urlopen("http://www.chainofgood.co.uk/passiton").read()
  soup = BeautifulSoup(htm, "html5lib")
  i = randint(0,101)
  compliment = soup.findAll('p')[i].getText()
  if name:
    compliment = name + ', ' + compliment
  yield from bot.coro_send_message(
      event.conv,
      _(compliment))

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
