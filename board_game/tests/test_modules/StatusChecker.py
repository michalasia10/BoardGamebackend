from typing import List

class StatusChecker:
    def __init__(self, matchesJson: dict):
        self._matchesJson = matchesJson

    def check_is_any_finished_status(self) -> bool:
        matches: List[dict] = self._matchesJson['matches']
        return any([match for match in matches if match['status']=='FINISHED'])
