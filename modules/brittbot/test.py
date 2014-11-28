#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/weissme.py - Weiss Me Nao

from modules.brittbot.filters import smart_ignore


@smart_ignore
def config_print(jenni, msg):
    import pdb; pdb.set_trace()
    jenni.reply("tested.")
    pass
config_print.rule = r"^test$"
config_print.priority = 'medium'
