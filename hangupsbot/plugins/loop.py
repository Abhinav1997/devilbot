import hangups
import plugins

def _initialise(bot):
  plugins.register_user_command(["loop"])

def loop(bot, event, *args):
  word = ' '.join(args).strip()
  if not word:
    word = "loop"
  count = 25
  while count > 0:
    yield from bot.coro_send_message(
        event.conv,
        _(word))
    count = count - 1
