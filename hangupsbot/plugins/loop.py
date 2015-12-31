import hangups
import plugins

def _initialise(bot):
  plugins.register_admin_command(["loop"])

def loop(bot, event, *args):
  word = ' '.join(args).strip()
  if not word:
    word = "ayy"
  while True:
    yield from bot.coro_send_message(
        event.conv,
        _(word))
