class HIDMapper:
    def __init__(self):
        self.history = []

    def generate_instructions(self, data) -> [str]:
        self.history.append(data)

        if data['target_name'] is None:
            return ['a_up']

        if data["health_bar"] > 1:
            return ["F2"]
        return ["F1", "F2"]

    def analise_instructions(self, instructions: [str]):
        for char in instructions:
            if char.startswith("a_"):
                return 2
