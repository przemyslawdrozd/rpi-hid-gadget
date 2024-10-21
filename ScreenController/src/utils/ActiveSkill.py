import time

ACTIVE_INTERVAL = 30  # Seconds


class ActiveSkill:
    def __init__(self):
        self.last_used_time = time.time()

    def check_interval(self) -> bool:
        current_time = time.time()
        if current_time - self.last_used_time >= ACTIVE_INTERVAL:
            self.last_used_time = current_time
            return True
        return False
