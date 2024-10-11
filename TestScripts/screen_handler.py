from health_bar import HealthBar
from fragment_screen_taker import FragmentScreenTaker
from cp_bar import CPBar
def main():
    fragment_screen_taker = FragmentScreenTaker()
    health_bar = HealthBar()
    cp_bar = CPBar()

    take_in_memory_image_buffer = fragment_screen_taker.take_screenshot_in_memory()

    res = health_bar.calculate_red_bar_percentage(take_in_memory_image_buffer)
    # res = health_bar.calculate_red_bar_percentage(take_in_memory_image_buffer)

    print("res", res)

if __name__ == "__main__":
    main()