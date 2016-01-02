import hangups
import plugins
import random
import os

def _initialise(bot):
  plugins.register_user_command(["compliment"])
    
def compliment(bot, event, *args):
  name = ' '.join(args).strip().title()
  with open(os.path.dirname(__file__) + "/compliments.txt") as f:
    compliment = f.readlines()
  if name:
    compliment = name + ', ' + random.choice(compliment)
  yield from bot.coro_send_message(
      event.conv,
      _(compliment.rstrip('\n')))
