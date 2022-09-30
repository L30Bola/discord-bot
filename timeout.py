from os import getenv

timeout_timer = float(getenv("TIMEOUT_TIMER"))


class Timeout:
    def __init__(self):
        self._is_timing_out: bool = False
        self._timer: float = timeout_timer
        self._interrupt_by_undeafen: bool = False
        self._interrupt_by_afk_channel_move: bool = False

    @property
    def is_timing_out(self):
        return self._is_timing_out

    @is_timing_out.setter
    def is_timing_out(self, value: bool):
        self._is_timing_out = value

    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value: float):
        self._timer = value

    @property
    def interrupt_by_undeafen(self):
        return self._interrupt_by_undeafen

    @interrupt_by_undeafen.setter
    def interrupt_by_undeafen(self, value: bool):
        self._interrupt_by_undeafen = value

    @property
    def interrupt_by_afk_channel_move(self):
        return self._interrupt_by_afk_channel_move

    @interrupt_by_afk_channel_move.setter
    def interrupt_by_afk_channel_move(self, value: bool):
        self._interrupt_by_afk_channel_move = value
