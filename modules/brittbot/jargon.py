#!/usr/bin/env python
# encoding: utf-8
# jenni brittbot/jargon.py - Technically sound advice

import random


def tech_jargon(jenni, msg):
    jargon = {
        "abbreviations": [
            "TCP", "HTTP", "SDD", "RAM", "GB", "CSS", "EMC", "GND", "VCC",
            "SSL", "AGP", "SQL", "FTP", "PCI", "AI", "ADP", "RSS", "XML", "EXE",
            "COM", "HDD", "THX", "SMTP", "SMS", "USB", "PNG", "PGP", "GPG", "HTTPS",
            "GIT", "TFS", "SVN", "RBAC", "LDAP", "AD", "HTML", "IP", "IRC", "NIC",
            "HTMLS", "PnP", "AJAX", "JSON", "HOCON", "ZIP", "TAR", "SATA3", "SATA2",
            "PATA", "VLC", "GSM", "CDMA", "GEOIP", "JVM", "OSX", "HS256", "YAML",
            "AIO", "PE", "OSCON",
        ],
        'adjectives': [
            "auxiliary", "primary", "back-end", "digital", "enterprise",
            "open-source", "virtual", "cross-platform", "redundant", "online",
            "haptic", "multi-byte", "bluetooth", "wireless", "1080p", "neural",
            "optical", "solid state", "mobile", "multi-threaded", "high fidelity",
            "haskell", "python", "postgresql", "MySql", "java", "javascript",
            "node.js", "github", "reverse", "crypto", "dimensional", "temporal",
            "quantum", "feedback", "anomalous", "ruby", "clojure", "c++", "golang",
            "concurrent",
        ],
        'nouns': [
            "driver", "protocol", "bandwidth", "panel",
            "microchip", "program", "port", "card", "array", "interface", "system",
            "sensor", "firewall", "hard drive", "pixel", "alarm", "feed", "monitor",
            "application", "transmitter", "bus", "circuit", "capacitor", "matrix",
            "mainframe", "keyboard", "input device", "sensor", "transistor", "ram disk",
            "system clock", "tree", "byte", "bytecode", "firewire", "link", "cache",
            "dot matrix", "cache matrix", "variable", "cable", "server", "error",
            "core", "module", "terminal", "conduit", "field", "drone", "subroutines",
            "puppet strings", "puppet", "hiera", "bitcoin", "cold brew",
            "magic the gathering", "solaris", "leatherman", "catalog", "brittbot",
            "agent", "custom fact", "custom type", "provider",
            "RedHat Enterprise Linux", "Windows", "cfactor", "gcc",
            "the pry debugger", "pusheen",
        ],
        'verbs': [
            "back up", "bypass", "hack", "override", "compress",
            "copy", "navigate", "index", "connect", "generate", "quantify",
            "calculate", "synthesize", "input", "transmit", "program", "reboot",
            "parse", "map", "degauss", "decouple", "download", "program", "upload",
            "couple", "partition", "obfuscate", "recurse", "invert", "increase",
            "decrease", "fluctuate", "jump", "kick", "restart", "compile", "serialize",
            "deserialize", "encode", "reencode", "decode", "decompile", "encrypt",
            "pixelate", "process", "energize", "cause", "handle", "break", "update",
            "cloak", "apply", "converge", "sync", "reverse engineer"
        ],
        'ingverbs': [
            "backing up", "bypassing", "hacking",
            "overriding", "compressing", "copying", "navigating", "indexing",
            "connecting", "generating", "quantifying", "calculating", "synthesizing",
            "inputting", "transmitting", "programming", "rebooting", "parsing",
            "mapping", "degaussing", "decoupling", "downloading", "programming",
            "uploading", "coupling", "partitioning", "obfuscating", "recursing",
            "inverting", "increasing", "decreasing", "fluctuating", "jumping",
            "kicking", "restarting", "compiling", "serializing", "deserializing",
            "encoding", "reencoding", "decoding", "decompiling", "encrypting",
            "pixelating", "processing", "energizing", "causing", "handling",
            "breaking", "updating", "cloaking", "torrenting", "converging",
            "devopsing", "executing", "chmod'ing", "syncing",
        ]
    }

    constructs = [{
        'types': ["verb", "noun", "abbreviation", "noun", "adjective", "abbreviation", "noun"],
        'structure': "If we {0} the {1}, we can get to the {2} {3} through the {4} {5} {6}!"
    }, {
        'types': ["verb", "adjective", "abbreviation", "noun"],
        'structure': "We need to {0} the {1} {2} {3}!"
    }, {
        'types': ["verb", "abbreviation", "noun", "verb", "adjective", "noun"],
        'structure': "Try to {0} the {1} {2}, maybe it will {3} the {4} {5}!"
    }, {
        'types': ["verb", "noun", "ingverb", "adjective", "abbreviation", "noun"],
        'structure': "You can't {0} the {1} without {2} the {3} {4} {5}!"
    }, {
        'types': ["adjective", "abbreviation", "noun", "verb", "adjective", "noun"],
        'structure': "Use the {0} {1} {2}, then you can {3} the {4} {5}!"
    }, {
        'types': ["abbreviation", "noun", "verb", "adjective", "noun", "verb", "abbreviation", "noun"],
        'structure': "The {0} {1} is down, {2} the {3} {4} so we can {5} the {6} {7}!"
    }, {
        'types': ["ingverb", "noun", "verb", "adjective", "abbreviation", "noun"],
        'structure': "{0} the {1} won't do anything, we need to {2} the {3} {4} {5}!"
    }, {
        'types': ["verb", "adjective", "abbreviation", "noun", "verb", "abbreviation", "noun"],
        'structure': "I'll {0} the {1} {2} {3}, that should {4} the {5} {6}!"
    }]

    get_words = lambda t: jargon[t + 's']
    get_word = lambda t: random.choice(get_words(t))

    sentence_format = random.choice(constructs)
    types = sentence_format['types']
    words = []
    for t in types:
        words.append(get_word(t))
    reply = sentence_format['structure'].format(*words)
    jenni.reply(reply)
tech_jargon.rule = r'(?i)^(?:!jargon|$nickname\S?.*what do you (?:think|know)\??)'
