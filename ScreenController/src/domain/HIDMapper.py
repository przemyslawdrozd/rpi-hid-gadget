class HIDMapper:
    def __init__(self):
        self.history = []

    def generate_instructions(self, data) -> [str]:
        self.history.insert(0, data)

        if len(self.history) > 5:
            self.history = self.history[:5]


        if data['target_name'] == "" :
            return ['a_up', 'F1']

        if data["health_bar"] > 1:
            return ["F2"]
        return ["F1", "F2"]

    def analise_instructions(self, instructions: [str]):
        for char in instructions:
            if char.startswith("a_"):
                return 2
        return 0
