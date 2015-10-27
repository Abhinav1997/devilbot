import hangups

import plugins

def _initialise(bot):
  plugins.register_user_command(["cookie"])
    
def cookie(bot, event, *args):
  name = ' '.join(args).strip().title()
  symbol =  u"\U0001f36a"
  cookies = name + ', ' + "have a cookie " + symbol
  yield from bot.coro_send_message(
      event.conv,
      _(cookies))
