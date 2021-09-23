from typing import Hashable, Any, Tuple
import random
import numpy as np
import time

from q_learner_saver.environments import Environment


class FindTargetEnvironment(Environment):

    WIN_REWARD = 25
    LOSE_REWARD = -300
    MOVE_REWARD = -1

    def __init__(self, sense, field_size=(8, 8)):
        super().__init__()
        self.player_pos = [0, 0]
        self.enemy_pos = [1, 1]
        self.target_pos = [2, 2]
        self.field_size = field_size  # width, height
        self.sense = sense
        self._indexed_moves = [self._move_up, self._move_right, self._move_down, self._move_left]

        # add action states
        self.add_actions(self._move_player_up, self._move_player_right, self._move_player_down, self._move_player_left)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['sense']
        return state

    def __setstate__(self, state, sense=None):
        self.__dict__.update(state)
        self.sense = None

    def step(
        self,
        action_index: int
    ) -> Tuple[Any, float, bool]:
        self._random_move_agent(self.enemy_pos)
        return super().step(action_index)

    def _get_state(self) -> Hashable:
        return (self.player_pos[0] - self.enemy_pos[0], self.player_pos[1] - self.enemy_pos[1]), \
               (self.player_pos[0] - self.target_pos[0], self.player_pos[1] - self.target_pos[1])

    def _finished(self) -> bool:
        return self.player_pos == self.target_pos or self.player_pos == self.enemy_pos

    def reset(self) -> Any:
        self.target_pos = [random.randint(0, self.field_size[0] - 1), random.randint(0, self.field_size[1] - 1)]
        self.player_pos = [random.randint(0, self.field_size[0] - 1), random.randint(0, self.field_size[1] - 1)]
        self.enemy_pos = [random.randint(0, self.field_size[0] - 1), random.randint(0, self.field_size[1] - 1)]
        self.sense.clear()

        # make sure that player and enemy pos are not the same
        while self.player_pos == self.enemy_pos or self.player_pos == self.target_pos:
            self.player_pos = [random.randint(0, self.field_size[0] - 1), random.randint(0, self.field_size[1] - 1)]
        return super().reset()

    def get_reward(self) -> float:
        if self.player_pos == self.target_pos:
            return self.WIN_REWARD
        elif self.player_pos == self.enemy_pos:
            return self.LOSE_REWARD
        else:
            return self.MOVE_REWARD

    def _random_move_agent(self, agent_pos):
        number = random.randint(0, 3)
        self._indexed_moves[number](agent_pos)  # noqa

    def state_representation(self) -> Any:
        self.sense.set_pixel(*self.target_pos, (0, 255, 0))
        self.sense.set_pixel(*self.enemy_pos, (255, 0, 0))
        self.sense.set_pixel(*self.player_pos, (200, 200, 200))
        time.sleep(0.1)
        return None

    def succes(self):
        return True if self.player_pos == self.target_pos else False

    def _move_player_up(self):
        if not self._finished():
            self._move_up(self.player_pos)

    def _move_player_right(self):
        if not self._finished():
            self._move_right(self.player_pos)

    def _move_player_down(self):
        if not self._finished():
            self._move_down(self.player_pos)

    def _move_player_left(self):
        if not self._finished():
            self._move_left(self.player_pos)

    def _move_up(self, agent_pos):
        self.sense.set_pixel(*agent_pos, (0, 0, 0))
        agent_pos[1] = max(0, agent_pos[1] - 1)

    def _move_right(self, agent_pos):
        self.sense.set_pixel(*agent_pos, (0, 0, 0))
        agent_pos[0] = min(self.field_size[0] - 1, agent_pos[0] + 1)

    def _move_down(self, agent_pos):
        self.sense.set_pixel(*agent_pos, (0, 0, 0))
        agent_pos[1] = min(self.field_size[1] - 1, agent_pos[1] + 1)

    def _move_left(self, agent_pos):
        self.sense.set_pixel(*agent_pos, (0, 0, 0))
        agent_pos[0] = max(0, agent_pos[0] - 1)
