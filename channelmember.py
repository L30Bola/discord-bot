from discord import Member
from os import getenv

timeout_timer = float(getenv("TIMEOUT_TIMER"))


class ChannelMember:
    def __init__(self, member: Member):
        self._discord_entity = member
        self._timeout_interrupt = False
        self._is_timing_out = False
        self._timeout_timer = timeout_timer

    @property
    def timeout_interrupt(self):
        return self._timeout_interrupt

    @timeout_interrupt.setter
    def timeout_interrupt(self, value: bool):
        self._timeout_interrupt = value

    @property
    def is_timing_out(self):
        return self._is_timing_out

    @is_timing_out.setter
    def is_timing_out(self, value: bool):
        self._is_timing_out = value

    @property
    def discord_entity(self):
        return self._discord_entity

    @discord_entity.setter
    def discord_entity(self, value: Member):
        self._discord_entity = value

    @property
    def timeout_timer(self):
        return self._timeout_timer

    @timeout_timer.setter
    def timeout_timer(self, value: int):
        self._timeout_timer = value
