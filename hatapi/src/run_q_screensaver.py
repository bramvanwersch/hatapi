import argparse
import pathlib
import os

from hatapi.src.q_learner_saver import q_learner
from hatapi.src.q_learner_saver import chaser_env

file_dir_path = pathlib.Path(__file__).parent.resolve()
TABLES_DIR = pathlib.Path(f"{file_dir_path}{os.sep}q_learner_saver{os.sep}tables{os.sep}")


def get_arg_parser():
    parser = argparse.ArgumentParser("Run a learning screensaver: ")
    parser.add_argument("-l", "--list_learners", help="List all learners that have been saved", action="store_true")
    parser.add_argument("-i", "--input", help="Name of a already learned learner. Default is None and will"
                                              " start a new learner", default=None)
    parser.add_argument("-e", "--show_every", help="Show every x generations what the learner looks like. Showing"
                                                   "all generations can mean very slow progression", default=100)
    parser.add_argument("-o", "--output", help="Name were the table is saved after shutdown. Leave it empty in order"
                                               "to not save the table.", default=None)
    return parser


def run_learning(sense, *args):
    parser = get_arg_parser()
    namespace = parser.parse_args(args)
    infile = namespace.input
    outfile = namespace.output
    show_every = namespace.show_every

    if namespace.list_learners is True:
        print("These are the available learners:")
        print_tables()
        return

    target_env = chaser_env.FindTargetEnvironment(sense, (8, 8))
    if infile is None and outfile is not None:
        if pathlib.Path(f"{TABLES_DIR}{os.sep}{outfile}.pickle").exists():
            total_ex = 1
            while True:
                answer = input("You are about to overwrite an existing learning table. Are you sure? (Y/N)")
                if answer.upper() == "Y":

                    break
                elif answer.upper() == "N":
                    return
                else:
                    print("Please type Y or N" + ("!" * total_ex))
                    total_ex += 1
    if infile is not None:
        try:
            learner = q_learner.QLearner.load(f"{TABLES_DIR}{os.sep}{infile}.pickle", sense)
            print(f"Loaded learner {infile}")
        except FileNotFoundError:
            print("No such input table available use one of:")
            print_tables()
            return
    else:
        learner = q_learner.QLearner(target_env, learning_rate=0.1, discount=0.9,
                                     action_mode="max", epsilon_decay=0.0001)
        print("Created new learner")
    try:
        print()
        print("Starting screensaver and learning...")
        print("Pres <Ctrl + C> to stop.")
        while True:
            learner.train(1, 100)
            if learner.total_generations % show_every == 0:
                learner.test(show_visual=True)
            else:
                learner.test(show_visual=False)
    except KeyboardInterrupt:
        if infile is not None:
            learner.save(f"{TABLES_DIR}{os.sep}{infile}.pickle")
            print(f"Saved table {infile}")
        elif outfile is not None:
            learner.save(f"{TABLES_DIR}{os.sep}{outfile}.pickle")
            print(f"Saved table {outfile}")


def print_tables():
    print(TABLES_DIR)
    paths = TABLES_DIR.rglob("*.pickle")
    for path in paths:
        print(path.stem)
