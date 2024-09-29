class HIDMapper:
    def __init__(self):
        self.history = []

    def generate_instructions(self, data) -> [str]:
        self.history.insert(0, data)

        if len(self.history) > 5:
            self.history = self.history[:5]

        if data['target_name'] == "" :
            return self._calculate_direction_with_thresholds(data)

        if data["health_bar"] > 1:
            return ["F2"]
        return ["F1", "F2"]

    def analise_instructions(self, instructions: [str]):
        for char in instructions:
            if char.startswith("a_"):
                return 2
        return 0
    
    def _calculate_direction_with_thresholds(self, data):
        target_dots = data['target_dots']
        current_direction = data.get('direction', 0)
        
        # Quadrant angles (in degrees)
        quadrant_angles = {
            'NE': 45,
            'SE': 135,
            'SW': 225,
            'NW': 315
        }
        
        # Get the quadrant with the most target dots
        best_quadrant = max(target_dots, key=target_dots.get)
        best_direction = quadrant_angles[best_quadrant]
        
        print("best_direction",best_direction) 
        # Define thresholds for direction matching the best quadrant
        if 315 <= best_direction or best_direction <= 45: # N
            # Best direction is upwards (North, +/- 45 degrees)
            if 315 <= current_direction or current_direction <= 45:
                return ['a_up', 'F1']  # Already pointing up
            elif 135 <= current_direction <= 225:
                return ['a_down', 'F1']  # Opposite (facing South)
            elif 45 < current_direction < 135:
                return ['a_right', 'F1']  # Turn right (facing East)
            elif 225 < current_direction < 315:
                return ['a_left', 'F1']  # Turn left (facing West)
            
        elif 135 <= best_direction <= 225:
            # Best direction is downwards (South, +/- 45 degrees)
            if 135 <= current_direction <= 225:
                return ['a_down', 'F1']  # Already pointing down
            elif 315 <= current_direction or current_direction <= 45:
                return ['a_up', 'F1']  # Opposite (facing North)
            elif 45 < current_direction < 135:
                return ['a_right', 'F1']  # Turn right (facing East)
            elif 225 < current_direction < 315:
                return ['a_left', 'F1']  # Turn left (facing West)
            
        elif 45 < best_direction < 135:
            # Best direction is right (East, +/- 45 degrees)
            if 45 < current_direction < 135:
                return ['a_right', 'F1']  # Already pointing right
            elif 135 <= current_direction <= 225:
                return ['a_down', 'F1']  # Turn down (facing South)
            elif 315 <= current_direction or current_direction <= 45:
                return ['a_up', 'F1']  # Turn up (facing North)
            elif 225 < current_direction < 315:
                return ['a_left', 'F1']  # Turn left (facing West)
            
        elif 225 < best_direction < 315:
            # Best direction is left (West, +/- 45 degrees)
            if 225 < current_direction < 315:
                return ['a_left', 'F1']  # Already pointing left
            elif 135 <= current_direction <= 225:
                return ['a_down', 'F1']  # Turn down (facing South)
            elif 45 < current_direction < 135:
                return ['a_right', 'F1']  # Turn right (facing East)
            elif 315 <= current_direction or current_direction <= 45:
                return ['a_up', 'F1']  # Turn up (facing North)
        
        # If no matching direction, return a default
        return ['Release', 'F1']