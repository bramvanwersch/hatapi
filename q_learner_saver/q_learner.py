import random
import matplotlib.pyplot as plt
import pickle

from q_learner_saver import environments


class QLearner:

    environment: environments.Environment

    def __init__(self, environment, discount=0.9, learning_rate=0.9, epsilon=0.9, epsilon_decay=0.001,
                 max_tries=200, action_mode="weighted"):
        self.total_generations = 0
        self._discount = discount
        self._learning_rate = learning_rate
        self._epsilon = epsilon
        self._epsilon_decay = 1 - epsilon_decay
        self.q_table = {}
        self.environment = environment
        self._all_actions = range(self.environment.nr_possible_actions())
        self._max_tries = max_tries
        self._action_mode = action_mode
        self._last_rewards = []

        self._training_rewards = []
        self._training_generations = []

    def train(self, nr_generations, report_rate=100, verbose=True):
        rewards = []
        for generation_nr in range(nr_generations):
            state = self.environment.reset()

            total_generation_reward = 0

            for i in range(self._max_tries):
                action_probabilities = self.get_action_probabilities(state)

                action = self.get_action(action_probabilities)
                next_state, reward, done = self.environment.step(action)

                total_generation_reward += reward

                # Q-formulat calculation
                next_action_probabilities = self.get_action_probabilities(next_state)
                best_next_action = self.get_max_action(next_action_probabilities)
                td_target = reward + self._discount * self.q_table[next_state][best_next_action]
                td_delta = td_target - self.q_table[state][action]
                self.q_table[state][action] += self._learning_rate * td_delta

                if done:
                    break
                state = next_state
            rewards.append(total_generation_reward)
            if report_rate != 0 and self.total_generations != 0 and self.total_generations % report_rate == 0:
                if verbose:
                    print(f"Simulation ran for {self.total_generations} generations")
                    if len(self._last_rewards) > 0:
                        print(f"Average reward: {sum(self._last_rewards) / len(self._last_rewards)}")
                self._last_rewards = []
            self._epsilon *= self._epsilon_decay
        self.total_generations += nr_generations
        self._last_rewards.extend(rewards)

    def test(self, show_visual=False):

        state = self.environment.reset()
        for i in range(self._max_tries):
            action_probabilities = self.get_action_probabilities(state)

            action = self.get_max_action(action_probabilities)
            next_state, reward, done = self.environment.step(action)

            # give a visual of the environment or get the reward
            state_presentation = self.environment.state_representation(show_visual=show_visual)
            if state_presentation is not None:
                print(state_presentation)
            if done:
                break
            state = next_state

    def show_reward_progress(self):
        plt.plot(self._training_generations, self._training_rewards)
        plt.show()

    def get_action_probabilities(self, state):
        if state not in self.q_table:
            self.q_table[state] = [random.random() for _ in range(self.environment.nr_possible_actions())]
        if self._epsilon > random.random():
            return [random.random() for _ in range(self.environment.nr_possible_actions())]
        else:
            return self.q_table[state]

    def get_action(self, action_probabilities):
        if self._action_mode == "weighted":
            return self.get_wheighted_action(action_probabilities)
        elif self._action_mode == "max":
            return self.get_max_action(action_probabilities)
        else:
            raise ValueError(f"No action mode {self._action_mode}.")

    def get_max_action(self, action_probabilities):
        highest_index = 0
        for index in range(len(action_probabilities)):
            if action_probabilities[index] > action_probabilities[highest_index]:
                highest_index = index
        return highest_index

    def get_wheighted_action(self, action_probabilities):
        offset = min(action_probabilities)
        positive_wheights = [num - offset + 1 for num in action_probabilities]
        return random.choices(range(len(action_probabilities)), positive_wheights, k=1)[0]

    def save(self, file_name):
        # save the q-table
        with open(file_name, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file_name, sense):
        with open(file_name, "rb") as f:
            instance = pickle.load(f)
        instance.environment.sense = sense
        return instance
