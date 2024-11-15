import logging
from enum import Enum
from ..consts import LOGGER_NAME
from ..utils.ConsoleLog import ConsoleLog

logger = logging.getLogger(LOGGER_NAME)

class Actions(Enum):
    SEARCH_TARGET = "SEARCH"
    FOUND_TARGET = "FOUND"
    ATTACK = "ATTACK"
    LOOT = "LOOT"
    REGEN = "REGEN"

class MageV2:
    def __init__(self):
        self.cl = ConsoleLog()
        self.data = []
        self.delay = 0

        self.current_action = Actions.SEARCH_TARGET.value

        self.current_search = 0
        self.search_threashold = 2
        self.first_search = True
        self.distance = 0
        self.searching = 0

        self.init_hit = False
        self.attack_threshold = 1
        self.current_attack = 0

        self.step = False
        self.found_invalid = False


    async def handle_mage_action(self, data: dict) -> [str]:
        try:
            self.data = data
            instructions = []

            match self.current_action:
                case Actions.SEARCH_TARGET.value:
                    instructions = self.__handle_search()
                case Actions.FOUND_TARGET.value:
                    instructions = self.__handle_found()
                case Actions.ATTACK.value:
                    instructions = self.__handle_attack()
                case Actions.LOOT.value:
                    instructions = self.__handle_loot()

            if len(instructions) == 0:
                instructions = ["Esc"]

            self.__table_info(instructions)
            return instructions, self.delay
        
        except Exception as e:
            logger.error(f"handle_mage_action error: {e}", exc_info=True)
            return ["Release"]

    def __handle_search(self):
        self.distance = 0
        self.searching += 1

        if self.step and self.searching == 5:
            self.step = False
            self.delay = 1
            return ["a_down"]

        if self.data["health_bar"] > 99:
            self.delay = 0.8
            self.current_action = Actions.FOUND_TARGET.value
            return ["F5"] 
        
        self.delay = 0.5
        if self.current_search == 0:
            self.__increase_search()

            hit = "Release"
            if self.first_search:
                hit = "F5"
                if self.data["char_hp"] < 100:
                    hit = ["F7"]
            return ["F1", hit]
        
        self.first_search = False

        if self.current_search == 1:
            self.__increase_search()
            return ["F2"]
        
        if self.current_search == 2:
            self.__increase_search()
            return ["F3"]
        
    def __handle_found(self):
        self.distance = self.distance + 1
        
        if not self.found_invalid and (self.data["chat"]["is_invalid"] or self.data["chat"]["is_cannot_see"] or self.data["chat"]["is_distance"]):
            self.found_invalid = True
            return ["F9"]
        self.found_invalid = False
        
        if self.init_hit:
            self.delay = 0.2
            self.current_action = Actions.ATTACK.value
            return ["F5"]

        if self.data["health_bar"] < 99:
            self.current_action = Actions.SEARCH_TARGET.value
            return ["Release"]

        self.init_hit = self.data["chat"]["is_use"]
        return ["F5"]

    def __handle_attack(self):
        self.current_search = 0

        if not self.found_invalid and (self.data["chat"]["is_invalid"] or self.data["chat"]["is_cannot_see"] or self.data["chat"]["is_distance"]):
            self.found_invalid = True
            return ["F9"]
        self.found_invalid = False

        if self.data["health_bar"] < 1:

            # LOOT_PACE 
            
            # self.delay = 0.7 # Short attack
            self.delay = 2.5 # Long attack
            self.current_action = Actions.LOOT.value
            return ["F9"]

        return self.__return_attack()
    
    def __handle_loot(self):
        self.searching = 0
        self.current_attack = 0
        self.init_hit = False
        self.step = True
        self.delay = 0
        self.current_action = Actions.SEARCH_TARGET.value
        return ["F10","F10","F10","F10","F10"]


    def __increase_search(self):
        if self.current_search == self.search_threashold:
            self.current_search = 0
        else:
            self.current_search += 1


    def __return_attack(self):
        self.delay = 1
        self.__increase_attack()

        if self.data["char_hp"] < 100:
            return ["F7", "a_down", "F5"]

        if self.current_attack == 0:
            return ["F5"]
        if self.current_attack == 1:
            return ["F6"]
        
        return ["F5"]
    

    def __increase_attack(self):
        if self.current_attack == self.attack_threshold:
            self.current_attack = 0
        else:
            self.current_attack =+ 1


    def __table_info(self, instructions: [str]) -> None:
        data = {
            "CP / HP / MP": f"{self.data["char_cp"]} / {self.data["char_hp"]} /  {self.data["char_mp"]}",
            "Action": self.current_action,
            
            # "SIT": self.rest_mode,
            # "TV": self.data["is_tv"],
            # "Anti": self.data["is_anti"],
            
            "Target HP": self.data["health_bar"],
            "delay": self.delay,
            "Distance": self.distance,
            "Searhing": self.searching,
            "Invalid": self.found_invalid,

            # "D is_valid": self.data["chat"]["is_invalid"],
            # "D is_cannot_see": self.data["chat"]["is_cannot_see"],
            # "D is_distance": self.data["chat"]["is_distance"]
            # "T Name": self.data["target_name"],
            # "T Search": self.current_search,
            # "T Is Found": self.is_found_target,
            # "Invalid": self.found_invalid,
            
            # "Spell": self.current_attack,
            # "Try Attack": self.is_try_attack,
            # "Init Attack": self.data["is_cast"],
            # "Fast Loot": self.fast_loot,
            # "Count hits": self.try_count,
            
        }

        self.cl.log(data, instructions)