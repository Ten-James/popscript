from src.optimalizations.Analysis import to_detailed_actions, to_actions
from src.optimalizations.ReadOptimalization import ReadOptimalization

def process(lines:list[str]) -> list[str]:
    detailed = to_detailed_actions(lines)
    detailed = ReadOptimalization(detailed)
    return to_actions(detailed)