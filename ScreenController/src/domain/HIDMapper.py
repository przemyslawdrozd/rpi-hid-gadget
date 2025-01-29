import re
import argparse
from ..utils.Anti import Anti
from ..utils.ActiveSkill import ActiveSkill
from ..domain.Mage import Mage
from ..domain.MageV2 import MageV2
from ..domain.Recharge import Recharge
from ..domain.Male import Male
from ..domain.Archer import Archer

DIRECTION_THRESHOLD = 40

DIRECTION_MAP = {
    "NE": 45,
    "SE": 135,
    "SW": 225,
    "NW": 315
}

# OWN_CHAR_NAME = r"Za\b"
OWN_CHAR_NAME = r"77\b"

NEXT_TAGET_MODULO = 3

class HIDMapper:
    def __init__(self, anti: Anti, args: argparse.Namespace):
        self.active_skill = ActiveSkill()
        self.mage = Mage()
        self.magev2 = MageV2(args)
        self.recharge = Recharge(args)
        self.male = Male(args)
        self.arch = Archer(args)
        self.anti = anti
        self.history = []
        self.args = args
        self.assist_status = None
        self.it_status = True

        self.ms_current_next_target = 1
        self.hit_flag = True

    async def generate_instructions(self, data) -> [str]:
        self.history.insert(0, data)

        # if data["is_anti"]:
        #     return self.anti.handle_action()

        # if data["is_tv"]:
        #     return ["Release"]
        
        # Search for the pattern with case insensitivity
        if self.__handle_own_name(data):
            return ["Release"]
        
        # if data["char_cp"] < 100:
        #     return ["Release"], 10
        
        if self.args.male:
            # return await self.mage.handle_mage_action(data)
            return await self.male.handle_male_action(data)
        
        if self.args.arch:
            # return await self.mage.handle_mage_action(data)
            return await self.arch.handle_arch_action(data)
        
        if self.args.mage:
            # return await self.mage.handle_mage_action(data)
            return await self.magev2.handle_mage_action(data)

            return instruction

        if self.args.ee:
            return await self.recharge.handle_recharge_action(data)

        if self.args.ms:
            if data['target_name'] != "" and data["health_bar"] < 1:
                return ["Esc", "Release"]
            # return ["F2", "F2", "F4"]
            # Spider
            return ["F1", "F2", "F1", "F2", "F1", "F2", "F3"], 0

            # Academy
            return ["F2", "F4"]
            # return ["F1", "F2", "F3", "F1", "F2", "F3", "F1", "F2","F3","F1", "F2","F3","F1", "F2","F3", "F1", "F2","F3", "F4"]
            return self.__handle_magic_short_range(data)

        if self.active_skill.check_interval():
            return ["F5"]

        if self.args.assist:
            return self.__handle_assist_mode(data)

        if len(self.history) > 5:
            self.history = self.history[:5]

        if data['target_name'] == "":
            if self.args.it:
                return self.__handle_it_mode()
            
            instructions = self._calculate_direction(data)
            instructions.append("F1")
            return instructions

        self.it_status = True

        if data["health_bar"] > 1:
            return ["F2"]
        return ["F1", "F2"]

    def __handle_assist_mode(self, data):
        if data["health_bar"] < 1:
            return ["F8", "F8", "F9"]

        return ["F2"]
    
    def __handle_it_mode(self):
        if  self.it_status:
            self.it_status = False
            return ["a_down", "F1"]
        return ["F1"]
    
    def __handle_own_name(self, data):
        # Search for the pattern with case insensitivity
        match = re.search(OWN_CHAR_NAME, data["target_name"], re.IGNORECASE)

        if match:
            return True
        return False
    
    def __handle_magic_short_range(self, data):
        # if data['target_name'] == "" and data["health_bar"] < 1:
        #     instructions = self._calculate_direction(data)
        #     instructions.append("F1")
        #     return instructions

        if data['target_name'] != "" and data["health_bar"] < 1:
            return ["F4", "F3"]
        
        if data['target_name'] == "":
            return ["F1"]
        
        return ["F2"]

    @staticmethod
    def analise_instructions(instructions: [str]) -> int:
        for char in instructions:
            if char.startswith("a_"):
                return 2
        return 0

    def _calculate_direction(self, data) -> [str]:
        target_dots = data['target_dots']
        current_direction = data['direction']

        # Find the quadrant with the highest target dot count
        max_target_quadrant = max(target_dots, key=target_dots.get)
        max_target_count = target_dots[max_target_quadrant]

        # If all targets are zero, return default action
        if max_target_count == 0:
            return ["F1"]

        # Get the expected direction for the quadrant with the highest target count
        expected_direction = DIRECTION_MAP[max_target_quadrant]

        # Check if the current direction is within the threshold of the expected direction
        if abs(expected_direction - current_direction) <= DIRECTION_THRESHOLD:
            return ["a_up"]
        # Check if the current direction is in the opposite quadrant
        elif abs((expected_direction + 180) % 360 - current_direction) <= DIRECTION_THRESHOLD:
            return ["a_down"]
        # Determine whether to turn right or left based on the difference between current and expected direction
        else:
            difference = (expected_direction - current_direction + 360) % 360
            if difference > 180:
                return ["a_left", "a_up"]  # Turn left if the difference is greater than 180 degrees
            else:
                return ["a_right", "a_up"]  # Turn right if the difference is less than or equal to 180 degrees
