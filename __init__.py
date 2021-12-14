# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.
import json

import requests
from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder


class FindMyPhoneSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""

    @intent_handler(IntentBuilder("FindPhone").require("Find").require("Phone").require("PhoneName").build())
    def handle_find_phone_intent(self, message):
        key = ""

        phone_name = message.data.get('PhoneName')

        if self.settings.get('phone_1_name') is not None \
                and phone_name == self.settings.get('phone_1_name').lower():
            key = self.settings.get('phone_1_key')
        elif self.settings.get('phone_2_name') is not None \
                and phone_name == self.settings.get('phone_2_name').lower():
            key = self.settings.get('phone_2_key')

        if key is None or key == "":
            self.speak_dialog("no phone found by that name")
        else:
            self.handle_request(key, phone_name)

    def stop(self):
        pass

    def handle_request(self, key, name):
        self.turn_up_ringtone(key)
        self.call_phone(key)
        self.speak_dialog("Calling " + name)

    def turn_up_ringtone(self, key):
        url = 'https://maker.ifttt.com/trigger/my_croft_turn_on_ringtone/with/key/' + key
        requests.get(url)

    def call_phone(self, key):
        url = 'https://maker.ifttt.com/trigger/my_croft_call_phone/with/key/' + key
        requests.get(url)


def create_skill():
    return FindMyPhoneSkill()
