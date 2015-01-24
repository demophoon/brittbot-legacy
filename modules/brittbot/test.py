#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/weissme.py - Weiss Me Nao

from modules.brittbot.filters import smart_ignore


@smart_ignore
def config_print(jenni, msg):
    jenni.config.allowed_channels
    jenni.reply("tested.")
    pass
config_print.rule = r"^test$"
config_print.priority = 'medium'


@smart_ignore
def ohai(jenni, msg):
    jenni.config.allowed_channels
    jenni.reply("facter")
    pass
ohai.rule = r".*ohai.*"
ohai.priority = 'medium'
