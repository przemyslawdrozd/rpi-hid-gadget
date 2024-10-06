from health_bar import HealthBar
from fragment_screen_taker import FragmentScreenTaker
def main():
    fragment_screen_taker = FragmentScreenTaker()
    health_bar = HealthBar()

    take_in_memory_image_buffer = fragment_screen_taker.take_screenshot_in_memory()

    res = health_bar.calculate_red_bar_percentage(take_in_memory_image_buffer)
    print("res", res)

if __name__ == "__main__":
    main()