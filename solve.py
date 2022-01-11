from collections import Counter
from enum import Enum, auto

import numpy as np


class Constraint(Enum):
    correct = auto()
    absent = auto()
    present = auto()


def guess(solutions, other):
    probability = np.zeros((5, 26))
    for i in range(5):
        letters, counts = zip(*Counter(ord(s[i]) - ord('a') for s in solutions).most_common())
        probability[i, letters] = counts
    probability /= len(solutions)

    words = solutions + other
    metric = (tuple(ord(c) - ord('a') for c in w) for w in words)
    metric = (probability[range(5), m].sum() for m in metric)
    return max(zip(metric, words), key=lambda w: w[0])[1]


def constrain(solutions, other, current, constraints):
    for i in range(5):
        match constraints[i]:
            case Constraint.correct:
                solutions = [w for w in solutions if w[i] == current[i]]
                other = [w for w in other if w[i] == current[i]]

            case Constraint.absent:
                solutions = [w for w in solutions if w[i] != current[i]]
                other = [w for w in other if w[i] != current[i]]

            case Constraint.present:
                solutions = [w for w in solutions if w[i] != current[i] and current[i] in w]
                other = [w for w in other if w[i] != current[i] and current[i] in w]

    return solutions, other
