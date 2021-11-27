
from q_learner_saver import q_learner
from q_learner_saver import chaser_env


def run_learning(sense, continue_=False):
    target_env = chaser_env.FindTargetEnvironment(sense, (8, 8))
    print("Pres <Ctrl + C> to stop.")
    if continue_ is not False:
        learner = q_learner.QLearner.load("q_learner_saver/tables/target_chase.pickle", sense)
    else:
        learner = q_learner.QLearner(target_env, learning_rate=0.1, discount=0.9,
                                     action_mode="max", epsilon_decay=0.0001)
    try:
        while True:
            learner.train(1, 100)
            learner.test()
    except KeyboardInterrupt:
        learner.save("q_learner_saver/tables/target_chase.pickle")
