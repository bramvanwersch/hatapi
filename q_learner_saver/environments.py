from abc import ABC, abstractmethod
from typing import Tuple, Any, Callable, Hashable, List


class Environment(ABC):
    _action_states: "ActionStates"
    steps_taken: int

    def __init__(self):
        self._action_states = ActionStates()
        self.steps_taken = 0

    def add_actions(
        self,
        *functions: Callable
    ):
        for function in functions:
            action_state_function = ActionStateFunction(self, function)
            self._action_states.add(action_state_function)

    def step(
        self,
        action_index: int
    ) -> Tuple[Any, float, bool]:
        self.steps_taken += 1
        # call the action
        reward = self._action_states[action_index]()
        return self._get_state(), reward, self._finished()

    @abstractmethod
    def _get_state(self) -> Hashable:
        pass

    @abstractmethod
    def _finished(self) -> bool:
        pass

    @abstractmethod
    def reset(self) -> Any:
        # reset the envionment and return the current state
        self.steps_taken = 0
        return self._get_state()

    def nr_possible_actions(self) -> int:
        return len(self._action_states)

    def state_representation(self) -> Any:
        # return the representation of a state
        return self._get_state()

    @abstractmethod
    def get_reward(self, *args: Any) -> float:
        pass

    def succes(self):
        return self._finished()


class ActionStates:

    _actions: List["ActionStateFunction"]

    def __init__(self):
        self._actions = []

    def add(
        self,
        action: "ActionStateFunction"
    ):
        self._actions.append(action)

    def __getitem__(
        self,
        item: int
    ) -> "ActionStateFunction":
        return self._actions[item]

    def __len__(self) -> int:
        return len(self._actions)


class ActionStateFunction:
    """Make sure that when a Action state function is called a reward is forced to return"""

    _environment: "Environment"
    _function: Callable

    def __init__(
        self,
        environment: "Environment",
        function: Callable
    ):
        self._environment = environment
        self._function = function

    def __call__(
        self,
        *args,
        **kwargs
    ) -> float:
        return_args = self._function(*args, **kwargs)
        if return_args is None:
            return self._environment.get_reward()
        return self._environment.get_reward(return_args)
