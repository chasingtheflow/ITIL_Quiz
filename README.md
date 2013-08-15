ITIL Quiz
=========
A little python utility for ITIL v3 Foundations practice exams.

Installation
------------
For installation instructions visit [the project site](http://chasingtheflow.github.io/ITIL_Quiz/).

Creating Quizzes
----------------
Creating your own quiz file is relatively straightforward. Questions are broken down into a few different parts:
* The questions itself
* Any options associated with the question [optional]
* Possible answers
* The correct answer
* The explanation of the answer

Each question part resides on its own line prepended by an identifier. Discrete questions are separated by a single blank line.

Questions are prepended by `Q: ` as in:

    Q: Which of the following processes are concerned with managing risks to services?

Options are prepended with `O: ` and are pipe separated:

    O: IT service continuity management | Information security management | Service catalog management

Possible answers are prepended by a number followed by a period and space:

    1. All of the above
    2. 1 and 3 only
    3. 2 and 3 only
    4. 1 and 2 only

The correct answer is prepended by `A: ` followed by the number of the correct possible answer:

    A: 4

Explanations are prepended by `E: ` and will be shown if the user misses the question:

    E: Service continuity management carries out risk assessment as part of defining requirements and strategy. Information security also needs to analyze security risks before taking action to mitigate them. Service catalog management does not carry out these assessments.

It's important to note that linebreaks are important and there should be a space following each of the prepended identifiers. The quiz file ends with a single blank line after the final question. 
