import time

import plugins


def _initialise(bot):
    plugins.register_user_command(["tldr"])


def tldr(bot, event, *args):
    """Adds a short message to a list saved for the conversation using:
    /devilbot tldr <message>
    All TLDRs can be retrieved by /devilbot tldr, single tldr with /devilbot <number>
    All TLDRs can be deleted using /devilbot tldr clear, single tldr with /devilbot clear <number>"""
    parameters = list(args)

    if not bot.memory.exists(['tldr']):
        bot.memory.set_by_path(['tldr'], {})

    if not bot.memory.exists(['tldr', event.conv_id]):
        bot.memory.set_by_path(['tldr', event.conv_id], {})

    conv_tldr = bot.memory.get_by_path(['tldr', event.conv_id])

    display = False
    if not parameters:
        display = True
    elif len(parameters) == 1 and parameters[0].isdigit():
        display = int(parameters[0]) - 1

    if display is not False:
        # Display all messages or a specific message
        html = []
        for num, timestamp in enumerate(sorted(conv_tldr, key=float)):
            if display is True or display == num:
                html.append(_("{}. {} <b>{} ago</b>").format( str(num+1),
                                                             conv_tldr[timestamp],
                                                             _time_ago(float(timestamp)) ))

        if len(html) == 0:
            html.append(_("TL;DR not found"))
        else:
            html.insert(0, _("<b>TL;DR ({} stored):</b>").format(len(conv_tldr)))
        message = _("<br />".join(html))

        yield from bot.coro_send_message(event.conv_id, message)

        return

    if parameters[0] == "clear":
        if len(parameters) == 2 and parameters[1].isdigit():
            sorted_keys = sorted(list(conv_tldr.keys()), key=float)
            key_index = int(parameters[1]) - 1
            if key_index < 0 or key_index >= len(sorted_keys):
                message = _("TL;DR #{} not found").format(parameters[1])
            else:
                popped_tldr = conv_tldr.pop(sorted_keys[key_index])
                bot.memory.set_by_path(['tldr', event.conv_id], conv_tldr)
                message = _('TL;DR #{} removed - "{}"').format(parameters[1], popped_tldr)
        else:
            bot.memory.set_by_path(['tldr', event.conv_id], {})
            message = _("All TL;DRs cleared")

        yield from bot.coro_send_message(event.conv_id, message)

    else:
        tldr = ' '.join(parameters)
        if tldr:
            # Add message to list
            conv_tldr[str(time.time())] = tldr
            bot.memory.set_by_path(['tldr', event.conv_id], conv_tldr)
            yield from bot.coro_send_message( event.conv_id,
                                              _('<em>{}</em> added to TL;DR. Count: {}').format( tldr,
                                                                                                 len(conv_tldr) ))

    bot.memory.save()


def _time_ago(timestamp):
    time_difference = time.time() - timestamp
    if time_difference < 60: # seconds
        return _("{}s").format(int(time_difference))
    elif time_difference < 60*60: # minutes
        return _("{}m").format(int(time_difference/60))
    elif time_difference < 60*60*24: # hours
        return _("{}h").format(int(time_difference/(60*60)))
    else:
        return _("{}d").format(int(time_difference/(60*60*24)))
