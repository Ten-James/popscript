from src.optimalizations.Analysis import DetailedAction, matches, ACTION


def ReadRemoveRead(actions: list[DetailedAction]) -> list[DetailedAction]:
    """
    This optmalization removes duplicates read actions from code and use DUP instead
    from:
    READ a
    any -1 action
    READ a

    to:
    READ a
    DUP
    any -1 action
    """
    i = len(actions) - 3
    while i > 0:
        if matches(actions[i], action_type=ACTION.READ):
            j = i + 1
            if matches(actions[j], stack=-1):
                if matches(actions[j + 1], action_type=ACTION.READ, args=actions[i].args):
                    actions.pop(j + 1)
                    actions.insert(j, DetailedAction("DUP"))
        i -= 1
    return actions


def ReadOptimalization(actions: list[DetailedAction]) -> list[DetailedAction]:
    actions = ReadRemoveRead(actions)
    return actions
