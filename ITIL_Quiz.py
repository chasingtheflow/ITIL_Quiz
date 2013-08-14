#! usr/bin/env python2.7
# pylint: disable-msg=I0011,R0903,R0913
"""
A little cmd line app for studying ITIL

Usage: python quizzer.py a_quiz_file

"""

import os
import textwrap
import argparse
from random import shuffle


class Quiz:
    """An ITIL Foundations Quiz"""

    def __init__(self, args):
        """Load the quiz"""
        self.problems = []
        self.should_shuffle = args.shuffle
        self.parse_quiz_file(args.quiz[0])
        self.instructions = "\n" + \
            " Welcome to the ITIL Quiz game!\n\n" + \
            " This quiz will present you with 40 ITIL Foundations exam\n" + \
            " questions, followed by a summary of missed questions.\n\n" + \
            " Enter the <a>, <s>, <d>, & <f> keys to submit your answer.\n" + \
            " Enter <q> at any time to end the quiz.\n\n" + \
            " Press <Enter> when you're ready to begin...\n"

    def parse_quiz_file(self, quiz_file):
        """Parse a quiz file"""

        with open(quiz_file, "rU") as question_file:
            question = None
            choices = None
            answer = None
            explanation = None
            options = None
            choices = []

            for line in question_file.readlines():
                if line[0] == 'Q':
                    # Parsing a question
                    question = line[3:-1].strip()
                elif line[0] == "O":
                    # Question options [not every question will have]
                    options = [option.strip() for option
                               in line[3:-1].split("|")]
                elif line[0] in ['1', '2', '3', '4']:
                    # Parsing a possible answer
                    choices.append(line[3:-1].strip())
                elif line[0] == 'A':
                    # The correct answer
                    answer = line[3:-1].strip()
                elif line[0] == "E":
                    # The answer explanation
                    explanation = line[3:-1].strip()
                elif question is None:
                    # Parsed everything
                    break
                else:
                    # Create the problem object and reset vars
                    problem = Problem(question, choices, answer,
                                      explanation, options)
                    self.problems.append(problem)
                    question = None
                    choices = None
                    answer = None
                    explanation = None
                    options = None
                    choices = []

    def show_instructions(self):
        """Show instructions to the user"""
        clear_screen()
        print self.instructions

    def get_problems(self):
        """Generate problems"""
        if self.should_shuffle:
            shuffle(self.problems)
        for problem in self.problems:
            yield problem

    def get_user_input(self):  # pylint: disable=I0011,R0201
        """Return the input from the user"""
        return raw_input(" ~> ")

    def print_missed_problem_summary(self):
        """Prints the results of the quiz"""
        missed_problems = [problem for problem in self.problems
                           if problem.user_answered_incorrectly is True]
        unattempted_problems = [problem for problem in self.problems
                                if problem.user_answered_incorrectly is None]

        clear_screen()
        print

        for missed_problem in missed_problems:
            missed_problem.print_result()

        missed_count = len(missed_problems)
        unattempted_count = len(unattempted_problems)
        problem_count = len(self.problems)
        correct_count = problem_count - missed_count - unattempted_count
        attempted_count = problem_count - unattempted_count

        score = correct_count / (problem_count + 0.0) * 100

        if unattempted_count > 0:
            print("\n Score: {} / {} Missed: {}" +
                  " Attempted: {} {}%\n").format(correct_count,
                                                 problem_count,
                                                 missed_count,
                                                 attempted_count,
                                                 score)
        else:
            print("\n Score: {} / {} Missed: {}  {}%\n").format(correct_count,
                                                                problem_count,
                                                                missed_count,
                                                                score)

        if score == 100:
            print(" Damn, son. Nice work.")
        elif score >= 85:
            print(" Nice work.")
        elif score >= 75:
            print(" Gettin there.")
        elif score >= 65:
            print(" Meh, You Passed.")
        else:
            print(" All your base are belong to us.\n" +
                  "\n Try\n     Try\n         Again.")

    def play(self):
        """Play the quiz game"""
        while True:
            self.show_instructions()
            user_input = self.get_user_input()
            if user_input.strip() == "":
                break
            elif user_input.strip() in ["q", "Q"]:
                return

        keys = ['A', 'S', 'D', 'F', 'Q']
        number_of_problems = len(self.problems)
        current_problem_number = 1

        problem_generator = self.get_problems()

        for problem in problem_generator:
            clear_screen()
            print("\n Problem {} of {}:").format(current_problem_number,
                                                 number_of_problems)
            print(str(problem) + "\n")
            user_input = self.get_user_input().upper()

            while user_input not in keys:
                clear_screen()
                print("\n Problem {} of {}:").format(current_problem_number,
                                                     number_of_problems)
                print(str(problem) + "\n")
                print(" Enter <a>, <s>, <d>, <f> to answer, or <q> to quit.")
                user_input = self.get_user_input().upper()

            if user_input in ['q', 'Q']:
                break

            if keys.index(user_input) + 1 == int(problem.answer):
                problem.user_answered_incorrectly = False
            else:
                problem.user_answered_incorrectly = True

            problem.user_answer = user_input
            current_problem_number += 1

        self.print_missed_problem_summary()


class Problem:  # pylint: disable=I0011,R0902
    """An ITIL Problem object"""

    def __init__(self, question, choices, answer, explanation, options=None):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.explanation = explanation
        self.options = options
        self.user_answer = None
        self.user_answered_incorrectly = None
        self.keys = [' A', ' S', ' D', ' F']

    def __str__(self):
        return self.question_string()

    def print_result(self):
        """Print result."""
        print(self.question_string())
        print(" You answered:    {}").format(self.user_answer)
        print(" Correct Answer:  {}").format(self.keys[int(self.answer) - 1]
                                             .strip())

        wrapper = textwrap.TextWrapper(initial_indent=" ",
                                       subsequent_indent=" ",
                                       width=80).wrap

        print
        for line in wrapper(self.explanation):
            print line
        print

    def question_string(self):
        """Return human readable question string"""
        wrapper = textwrap.TextWrapper(initial_indent = " ",
        question_string = " " + self.question + "\n"
        if self.options is not None:
            for index,  option in enumerate(self.options):
                question_string += "  " + str(index + 1) + ". " + option + "\n"

        question_string += "\n"
        for index, choice in enumerate(self.choices):
            question_string += self.keys[index] + ") " + choice + "\n"

        return question_string


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
        

class Text_wrapper:
    __metaclass__ = Singleton

    def __init__(self, text):
        if not self.wrapper:
            self.wrapper = textwrap.TextWrapper(initial_indent = " ",
                                                subsequent_indent = " ",
                                                width=80).wrap
        for line in self.wrapper(text):
            yield line


def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Run the quizzer"""
    parser = argparse.ArgumentParser(description=
                                     'Practice ITIL v3 Foundations exams.')
    parser.add_argument('-s', '--shuffle',
                        action='store_true',
                        help='shuffle the order of the questions')
    parser.add_argument('quiz', metavar='quiz', nargs=1,
                        help='path to an ITIL quiz file')
    args = parser.parse_args()
    quizzer = Quiz(args)
    quizzer.play()


if __name__ == "__main__":
    main()
