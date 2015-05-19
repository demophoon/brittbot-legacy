#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/420.py - Get n0sc0ped.

import random

from modules.brittbot.filters import smart_ignore


commandments = [
    "Codmandment #1: Thou shalt smite noobs.",
    "Codmandment #2: Thou shalt refer to thy smited noobs as 'scrubs.'",
    "Codmandment #3: Thou shalt not use telesoping optics or other vision-enhancing devices.",
    "Codmandment #4: Thou shalt rotate an amount not beneath three-hundred sixty degrees before the smiting.",
    "Codmandment #5: Thou shalt use only the Holy Rifled Tube of Sniping or the Divine Blades as the tools of smiting.",
    "Codmandment #6: During thy smiting, thou shalt consume exclusively the Chip of the Holy Flavored Powder and the Green Liquid of Divine Energy.",
    "Codmandment #7: After the smiting, thou shalt place thy genitals in the Scrub's face repeatedly.",
    "Codmandment #8: After the genital-placing, thou shalt make salacious assertions about Scrub's mother, and detail thou's sexual acts with Scrub's mother.",
    "Codmandment #9: To prepare the Scrub, thou shalt describe in detail thou previous conquests and smitings in an intimidating and impressive manner.",
    "Codmandment #10: If thou ist ever offend by the Scrub, thou shalt question the Scrub's sexuality and assault the Scrub with verbal insults tailored to the Scrub's race, gender, and country of origin.",
    "Thou shalt smoke weed everyday.",
    "Praise it and blaze it.",
    "I am the Lord thy Clan, and thou shall have no other clans before [ME].",
    "Thou shalt make of your avatar any lameass images.",
    "Thou shalt not invite to [ME] clan in vain; no scrubs allows.",
    "Remember the lobby and keep it sacred; speakest foul, become exiled.",
    "Honor thy console and thy controller.",
    "Thou shall not teamkill.",
    "Thou shall not overcommit to the enemy.",
    "Thou shall not killsteal.",
    "Thou shall not pass bad weed to thy homies.",
    "Thou shall covet the scrublord's mom, his prestige, and his noobtube.",
    "The scrubs tasted the water but it had been turned into Mtn Dew.",
]

books = [
    "xX360quickscopezXx",
    "xXxSgtSkrublordxXx",
    "xXxCrystalFuckingWeedxXx",
]


@smart_ignore
def blaze_it(jenni, input):
    index = random.choice(range(len(commandments)))
    msg = "'%s' - The Book of %s 420: 6-9" % (
        commandments[index],
        books[index % len(books)],
    )
    jenni.say(msg)
blaze_it.rule = r".*\b(w?rekt|4/?20|n(o|0)sc(o|0)pe|360|b+l+a+z+e+ ?(i+t+|e+t+|d+a+t+)|we+ed.*(ev)?er(y|e)day|smoke.*we+ed)\b.*"
blaze_it.priority = 'medium'
