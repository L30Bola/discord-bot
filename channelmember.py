from discord import Member
from timeout import *


class ChannelMember:
    def __init__(self, member: Member):
        self._discord_entity: Member = member
        self._timeout: Timeout = Timeout()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: Timeout):
        self._timeout = value

    @property
    def discord_entity(self):
        return self._discord_entity

    @discord_entity.setter
    def discord_entity(self, value: Member):
        self._discord_entity = value
