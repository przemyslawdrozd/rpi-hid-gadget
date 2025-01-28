import logging
import random
import argparse

from enum import Enum
from ..consts import LOGGER_NAME
from ..utils.ConsoleLog import ConsoleLog
from datetime import datetime, timedelta
from ..utils.HPAlarm import HPAlarm
import time

logger = logging.getLogger(LOGGER_NAME)

SELF_CP = 100

START_REGEN = 20
END_REGEN = 80

VAMP_HP = 40
SELF_HEAL = 70 

class Actions(Enum):
    FOLLOW = "FOLLOW"
    RECHARGE = "RECHARGE"
    REST = "REST"
    HEAL = "HEAL"
    REGEN = "REGEN"

class Recharge:
    def __init__(self, args: argparse.Namespace):
        self.cl = ConsoleLog()
        self.alarm = HPAlarm()
        self.args = args
        self.data = []
        self.delay = 0
        
        self.start_at = None
        self.start_time = None
        self.working_time = None
        self.start_timer()

        self.current_action = Actions.FOLLOW.value

        self.rechanrge_count = 0
        self.searching = 0

        self.init_hit = False
        self.attack_threshold = 1
        self.current_attack = 0
        self.count_hits = 0

        self.found_invalid = False
        self.rest_mode = False
        self.hp_on_rest = 0

        self.apply_sleep = False
        self.adjust_view = True

    async def handle_recharge_action(self, data: dict) -> [str]:
        try:

            self.data = data
            instructions = []

            match self.current_action:
                case Actions.FOLLOW.value:
                    instructions = self.__handle_follow()
                    if self.adjust_view:
                        instructions.append("pageUp")
                        self.adjust_view = False
                case Actions.RECHARGE.value:
                    instructions = self.__handle_recharge()

                case Actions.REGEN.value:
                    instructions = self.__handle_regen()

            logger.debug(f"instructions: {instructions}")

            # sleep_instruction = self.__handle_sleep()

            if self.data["pt_hp"] < 40:
                instructions = ["F1", "F2"]

            # if sleep_instruction is not None:
            #     instructions = sleep_instruction

            if data["char_cp"] < SELF_CP or data["is_anti"]:
                instructions = ["Release"]
                self.delay = 3

            # instructions = ["F3"]
            # self.delay = 60

            self.update_working_time()
            self.__table_info(instructions)
            self.__alert()

            return instructions, self.delay
        
        except Exception as e:
            logger.error(f"handle_mage_action error: {e}", exc_info=True)
            return ["Release"], 10

    def __handle_follow(self):
        self.delay = 1
        self.current_action = Actions.RECHARGE.value
        return ["F1"]
    
    def __handle_recharge(self):
        self.delay = 3
        self.current_action = Actions.FOLLOW.value

        if self.data["char_hp"] < self.data["pt_mp"]:
            return ["F1"]

        if self.data["pt_mp"] < 50:
            return ["F3"]
        return ["Release"]


    def __handle_found(self):
        self.searching = 0
        self.distance = self.distance + 1
        self.delay = 0
        
        if not self.found_invalid and (self.data["chat"]["is_invalid"] or self.data["chat"]["is_cannot_see"] or self.data["chat"]["is_distance"]):
            self.found_invalid = True
            self.delay = 1
            return ["F9"]
        self.found_invalid = False
        

        if self.data["health_bar"] < 99 and not self.__init_hit():
            self.current_action = Actions.SEARCH_TARGET.value
            # return ["Esc", "Release"] # Use when single targate around
            return ["Esc", self.__move()]
        
        self.init_hit = self.__init_hit()
        if self.init_hit:
            self.current_action = Actions.ATTACK.value
            return self.__return_attack()

        return self.__return_attack()

    def __init_hit(self):
        if self.data["chat"]["is_use"] or self.data["chat"]["is_att"]:
            return True
        return False

    def __handle_attack(self):
        self.delay = 1
        self.current_search = 0
        self.count_hits = self.count_hits + 1
        self.apply_sleep = False
        self.adjust_view = True

        if not self.found_invalid and (self.data["chat"]["is_invalid"] or self.data["chat"]["is_cannot_see"] or self.data["chat"]["is_distance"]):
            self.found_invalid = True
            self.delay = 0
            return ["F9", "F10"]
        self.found_invalid = False

        if self.data["health_bar"] < 1:
            # LOOT_PACE 
            # self.delay = 0 # Short attack
            self.delay = 4 # Long attack
            self.current_action = Actions.LOOT.value

            # self.current_action = Actions.SEARCH_TARGET.value
            return ["F9"]
            # return ["F9", "F10", "F10", "F10"]

        return self.__return_attack()
    
    def __handle_loot(self):
        self.count_hits = 0
        self.current_attack = 0
        self.init_hit = False
        self.delay = 3

        # Comment to disable REGEN
        if self.data["char_mp"] < START_REGEN:
            self.current_action = Actions.REGEN.value
            return ["F10", "F10", "F10", "F10", "a_down"]

        self.current_action = Actions.SEARCH_TARGET.value
        return ["F10", "F10", "F10", "F10", "F10", "F10", "F10", "F10", "F10", "a_down"]
        # return ["F10", "F10", "F10", "F10", "F10", "F10", "F10", "F10", "F10", "F10"]

    def __handle_regen(self):
        self.delay = 2.5
        if self.data["char_mp"] < START_REGEN + 1 and not self.rest_mode:     
            self.rest_mode = True
            self.hp_on_rest = self.data["char_hp"]
            return ["F11", "Release"]

        if self.rest_mode and self.data["char_mp"] > END_REGEN:
            self.rest_mode = False
            self.delay = 0.5
            self.current_action = Actions.SEARCH_TARGET.value
            return ["F11", "Release"]

        if self.data["char_hp"] < self.hp_on_rest:
            self.rest_mode = False
            self.current_action = Actions.ATTACK.value
            self.delay = 0.5
            return ["F1", "F5"]

        return ["Release"]

    def __increase_search(self):
        if self.current_search == self.search_threashold:
            self.current_search = 0
        else:
            self.current_search += 1


    def __return_attack(self):
        self.delay = 1
        self.__increase_attack()

        if self.current_action == Actions.FOUND_TARGET.value:
            return ["F5"]
        
        return ["F6"]

        if self.data["char_hp"] < VAMP_HP:
            self.delay = 1.5
            return ["F7", "F1"]

        # if self.current_attack == 0:
        #     return ["F5", "F9"]
        # if self.current_attack == 1:
        #     return ["F6", "F9"]

        # if self.data["chat"]["is_sleep"] and not self.ss_applied:  
        #     self.ss_applied = True
        #     return ["F4", "F1", "F5"]
        return ["F5", "F6", "F10", "F10", "F10"]

        
        return ["F5", "F6"]
    
    def __handle_sleep(self):
        if not self.apply_sleep and self.data["chat"]["is_sleep"]:
            self.delay = 1
            self.apply_sleep = True
            return ["F4", "F1"]

    def __handle_heal(self):
        if self.data["char_hp"] < SELF_HEAL:
            return ["F8", "F1"]

    # def __handle_rebuff(self):
    #     self.delay = 10
    #     self.current_action = Actions.SEARCH_TARGET.value
    #     return ["F12"]
    
    def __move(self):
        # return "Release"
        return random.choice(["a_down", "a_up"])
        # return random.choice(["a_down"])

    def __increase_attack(self):
        if self.current_attack == self.attack_threshold:
            self.current_attack = 0
        else:
            self.current_attack =+ 1

    def __reset(self):
        if self.distance > 15 or self.searching > 15 or self.count_hits > 15:
            self.distance = 0
            self.searching = 0
            self.count_hits = 0
            return ["Esc", "a_down", "pageUp"]
        return None

    def format_seconds_to_hhmmss(self, seconds = 0):
        # Convert the float seconds to an integer for whole seconds
        seconds = int(seconds)
        # Use timedelta to format seconds into HH:MM:SS
        formatted_time = str(timedelta(seconds=seconds))
        return formatted_time

    def __table_info(self, instructions: [str]) -> None:
        data = {
            # "StartedAt": self.start_at,
            "Working:": self.format_seconds_to_hhmmss(self.working_time),
            "Delay": self.delay,
            "Anti": self.data["is_anti"] if self.args.anti else "Off",
            "CP / HP / MP": f"{self.data["char_cp"]} / {self.data["char_hp"]} /  {self.data["char_mp"]}",
            "Action": self.current_action,
            "PT HP/MP": f"{self.data["pt_hp"]} / {self.data["pt_mp"]}",
            # "SIT": self.rest_mode,
            # "TV": self.data["is_tv"],
            # "Anti": self.data["is_anti"],
            
            "Target HP": self.data["health_bar"],
            # "Dist": self.distance,
            # "Search": self.searching,
            "Hits": self.count_hits,
            # "Invalid": self.found_invalid,
            # "Sleep": self.data["chat"]["is_sleep"],
            

            # "D is_valid": self.data["chat"]["is_invalid"],
            # "D is_cannot_see": self.data["chat"]["is_cannot_see"],
            # "D is_distance": self.data["chat"]["is_distance"],
            # "D is_use": self.data["chat"]["is_use"]
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

    def __alert(self) -> None:
        if self.data["char_hp"] < 50:
            self.alarm.invoke_alert()


    def start_timer(self):
        # Record the start time as a formatted string
        self.start_at = datetime.now().strftime("%H:%M:%S")
        self.start_time = time.time()  # Record the start time in seconds for calculation
        print(f"Timer started at: {self.start_at}")

    def update_working_time(self):
        # Calculate the working time

        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.working_time = elapsed_time  # Keep it as a float for calculations
            formatted_working_time = str(timedelta(seconds=int(elapsed_time)))  # Format for display
            print(f"Working time: {formatted_working_time}")
        else:
            print("Timer has not been started.")