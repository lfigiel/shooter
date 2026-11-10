
import urllib.request
from pyray import *

def main():
    init_window(800, 550, "Xbox Gamepad Test")

    # Download the latest community controller mappings
    url = (
        "https://raw.githubusercontent.com/"
        "mdqinc/SDL_GameControllerDB/master/gamecontrollerdb.txt"
    )

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            mappings = response.read().decode("utf-8")

        result = set_gamepad_mappings(mappings)
        print("Gamepad mappings loaded:", result)

    except Exception as e:
        print("Could not load gamepad mappings:", e)

    set_target_fps(60)

    while not window_should_close():
        begin_drawing()
        clear_background(RAYWHITE)

        if is_gamepad_available(0):
            draw_text("CONNECTED", 30, 30, 20, GREEN)

            for i in range(18):
                pressed = is_gamepad_button_down(0, i)
                draw_text(
                    f"Button {i}: {pressed}",
                    30, 80 + i * 24, 16,
                    GREEN if pressed else GRAY
                )

            for i in range(6):
                value = get_gamepad_axis_movement(0, i)
                draw_text(
                    f"Axis {i}: {value:+.3f}",
                    350, 80 + i * 35, 18, BLUE
                )

        end_drawing()

    close_window()

if __name__ == "__main__":
    main()
