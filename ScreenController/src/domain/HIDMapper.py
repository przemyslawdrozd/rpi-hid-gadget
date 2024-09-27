class HIDMapper:
    def __init__(self):
        self.history = []

    def generate_instructions(self, data) -> [str]:
        self.history.append(data)

        if data["health_bar"] > 0:
            return ["F1"]
        return ["F1", "F2"]
