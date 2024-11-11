
import logging
import asyncio
from ..consts import LOGGER_NAME
from ..utils.ConsoleLog import ConsoleLog
logger = logging.getLogger(LOGGER_NAME)

class Mage:
    def __init__(self):
        self.cl = ConsoleLog()

        self.delay = 0

        self.search_repeat = False
        self.current_search = 0
        self.search_threashold = 2
        self.is_found_target = False

        self.is_attack = False
        self.try_count = 0

        self.current_attack = 0
        self.attack_threshold = 2

        self.rest_mode = False
        self.fast_loot = False

        self.found_invalid = False


    async def handle_mage_action(self, data):
        try:
            instructions = []
            self.data = data
            await self.__apply_delay()

            if not self.is_attack and self.data["char_mp"] < 1 and not self.rest_mode:
                instructions = self.__exec_actions()
                # instructions = self.__apply_is_rest_needed()
            else:
                instructions = self.__exec_actions()

            self.__table_info(instructions)

            return instructions
        except Exception as e:
            logger.error(f"handle_mage_action error: {e}", exc_info=True)
            return ["Release"]

    def __exec_actions(self):
        if self.rest_mode:
            return self.__apply_is_rest_needed()
        
        if not self.is_found_target:
            return self.find_target()

        attack_res = self.__first_attack()
        
        if attack_res is not None:
            return attack_res
        
        if self.data['target_name'] != "" and self.data["health_bar"] < 1 and self.is_attack:
            loot_res = self.__loot()
            self.fast_loot = False
            return loot_res
        
        if self.data['target_name'] == "" and self.data["health_bar"] < 1:
            return self.find_target()
        
        self.fast_loot = True
        if self.current_attack == 0:
                return ["F5"]
        if self.current_attack == 1:
                return ["F6"]
        if self.current_attack == 2:
                return ["F7"]
        
        return ["F5"]

    def __loot(self):
        self.is_attack = False
        self.is_found_target = False
        
        if self.fast_loot:
            self.delay = 0.5
            return ["F10"]

        self.delay = 2
        return ["F4"]

    def __first_attack(self):
        self.__increase_attack()
        if self.data['target_name'] != "" and self.data["health_bar"] > 99:
            self.delay = 1.2
            self.is_attack = True
            self.current_search = 0
            self.try_count = self.try_count + 1
            
            if not self.found_invalid and self.data["chat"]["is_invalid"] or self.data["chat"]["is_cannot_see"] or self.data["chat"]["is_distance"]:
                self.delay = 0.5
                self.found_invalid = True
                return ["F9"]

            self.found_invalid = False
            return ["F5"]

        return None
            
    def __apply_is_rest_needed(self):
        if self.data["char_mp"] < 1 and not self.rest_mode:
            self.rest_mode = True
            return ["F11", "Release"]
        
        if self.rest_mode and self.data["char_mp"] > 98:
            self.rest_mode = False
            self.delay = 0.5
            return ["F11", "Release"]
        
        return ["Release"]


    def find_target(self):
        self.delay = 0.3
        
        if self.data['target_name'] != "" and self.data["health_bar"] > 99:
            self.is_found_target = True
            return ["F5"] 

        if self.current_search == 0:
            self.__increase_seach()
            return ["F1", "Release"]
        
        if self.current_search == 1:
            self.__increase_seach()
            return ["F2", "Release"]
        
        if self.current_search == 2:
            self.__increase_seach()
            return ["F3","Release"]
        
    
    def __increase_seach(self):
        if self.current_search == self.search_threashold:
            self.current_search = 0
        else:
            self.current_search = self.current_search + 1
        logger.debug(f"current_search: {self.current_search}")
        
    def __swap_target(self):
        self.try_count = 0
        return ["F1", "Release"]

    def __increase_attack(self):
        if self.current_attack == self.attack_threshold:
            self.current_attack = 0
        else:
            self.current_attack = self.current_attack + 1

    async def __apply_delay(self):
        await asyncio.sleep(self.delay)
        self.delay = 0


    def __table_info(self, instructions):
        data = {
            # "CP": self.data["char_cp"],
            # "MP": self.data["char_mp"],
            # "SIT": self.rest_mode,
            # "TV": self.data["is_tv"],
            # "Anti": self.data["is_anti"],
            "Target HP": self.data["health_bar"],
            "Target Name": self.data["target_name"],
            "Is Invalid": self.found_invalid,
            "Search target": self.current_search,
            "Found target": self.is_found_target,
            "Attack": self.is_attack,
            "Fast Loot": self.fast_loot,
            "Count before hit": self.try_count,
            "delay": self.delay,
            
        }

        self.cl.log(data, instructions)