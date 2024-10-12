from ..utils.ActiveSkill import ActiveSkill


class HIDMapper:
    def __init__(self):
        self.active_skill = ActiveSkill()
        self.history = []
        self.directions_map = {
            'NE': 45,
            'SE': 135,
            'SW': 225,
            'NW': 315
        }

    def generate_instructions(self, data) -> [str]:
        self.history.insert(0, data)

        if data["is_tv"]:
            return ["Release"]

        if self.active_skill.check_interval():
            return ["F5", "F6"]

        if len(self.history) > 5:
            self.history = self.history[:5]

        if data['target_name'] == "":
            instructions = self._calculate_direction(data)
            instructions.append("F1")
            return instructions

        if data["health_bar"] > 1:
            return ["F2"]
        return ["F1", "F2"]

    @staticmethod
    def analise_instructions(instructions: [str]):
        for char in instructions:
            if char.startswith("a_"):
                return 2
        return 0

    def _calculate_direction(self, data):
        target_dots = data['target_dots']
        current_direction = data['direction']
        threshold = 20

        # Find the quadrant with the highest target dot count
        max_target_quadrant = max(target_dots, key=target_dots.get)
        max_target_count = target_dots[max_target_quadrant]

        # If all targets are zero, return default action
        if max_target_count == 0:
            return ["F1"]

        # Get the expected direction for the quadrant with the highest target count
        expected_direction = self.directions_map[max_target_quadrant]

        # Check if the current direction is within the threshold of the expected direction
        if abs(expected_direction - current_direction) <= threshold:
            return ["a_up"]
        # Check if the current direction is in the opposite quadrant
        elif abs((expected_direction + 180) % 360 - current_direction) <= threshold:
            return ["a_down"]
        # Determine whether to turn right or left based on the difference between current and expected direction
        else:
            difference = (expected_direction - current_direction + 360) % 360
            if difference > 180:
                return ["a_left", "a_up"]  # Turn left if the difference is greater than 180 degrees
            else:
                return ["a_right", "a_up"]  # Turn right if the difference is less than or equal to 180 degrees
