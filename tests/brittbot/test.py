#!/usr/bin/env python
# encoding: utf-8

import unittest
import testbot


class TestModules(unittest.TestCase):

    jenni = None

    def assert_response(self, msg, expected_response, hostmask=None):
        if not hostmask:
            hostmask = "example!user@localhost"
        actual_response = self.jenni.send(msg, hostmask=hostmask)
        self.assertEqual(actual_response, expected_response)

    def test_interjection(self):
        self.assert_response("{}!".format(self.jenni.nick), "example!")

    def test_mgs_alert(self):
        self.assert_response("!!!", "http://brittg.com/zMJpt")
        self.assert_response("!", "http://brittg.com/zMJpt")
        self.assert_response("noop!", "")

    def test_fixit(self):
        self.assert_response("fix it", "https://youtu.be/1Isjgc0oX0s")
        self.assert_response("fix it!", "https://youtu.be/1Isjgc0oX0s")
        self.assert_response("just fix it!", "https://youtu.be/1Isjgc0oX0s")
        self.assert_response("JUST FIX IT!", "https://youtu.be/1Isjgc0oX0s")
        self.assert_response("just fix not it!", "")


def setUpModule():
    TestModules.jenni = testbot.get_jenni("/home/britt/.jenni/default.py")

if __name__ == '__main__':
    unittest.main()
