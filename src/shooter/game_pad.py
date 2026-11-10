import urllib.request
from pyray import *

def main():
    # Initialize the window engine layout
    screen_width = 800
    screen_height = 550
    init_window(screen_width, screen_height, "Gamepad Signals (Direct Import)")

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

    # Slot 0 catches the first connected gamepad system
    gamepad_idx = 0

    # Layout mapping array for all standard DualShock 4 buttons
    buttons = [
        ("D-Pad Up", GAMEPAD_BUTTON_LEFT_FACE_UP),
        ("D-Pad Down", GAMEPAD_BUTTON_LEFT_FACE_DOWN),
        ("D-Pad Left", GAMEPAD_BUTTON_LEFT_FACE_LEFT),
        ("D-Pad Right", GAMEPAD_BUTTON_LEFT_FACE_RIGHT),
        ("Cross / X", GAMEPAD_BUTTON_RIGHT_FACE_DOWN),
        ("Circle / O", GAMEPAD_BUTTON_RIGHT_FACE_RIGHT),
        ("Square / []", GAMEPAD_BUTTON_RIGHT_FACE_LEFT),
        ("Triangle / /\\", GAMEPAD_BUTTON_RIGHT_FACE_UP),
        ("L1 Shoulder", GAMEPAD_BUTTON_LEFT_TRIGGER_1),
        ("R1 Shoulder", GAMEPAD_BUTTON_RIGHT_TRIGGER_1),
        ("L2 Trigger (Digital)", GAMEPAD_BUTTON_LEFT_TRIGGER_2),
        ("R2 Trigger (Digital)", GAMEPAD_BUTTON_RIGHT_TRIGGER_2),
        ("Share", GAMEPAD_BUTTON_MIDDLE_LEFT),
        ("Options", GAMEPAD_BUTTON_MIDDLE_RIGHT),
        ("L3 (Left Stick Click)", GAMEPAD_BUTTON_LEFT_THUMB),
        ("R3 (Right Stick Click)", GAMEPAD_BUTTON_RIGHT_THUMB),
    ]

    while not window_should_close():
        begin_drawing()
        clear_background(RAYWHITE)

        # Check if hardware layer detects a controller active
        if is_gamepad_available(gamepad_idx):
            try:
                device_name = get_gamepad_name(gamepad_idx).decode('utf-8')
            except Exception:
                device_name = "Generic Controller Setup"

            draw_text("Gamepad Status: CONNECTED", 30, 20, 20, DARKGREEN)
            draw_text(f"Device Identity: {device_name}", 30, 45, 14, GRAY)

            # --- 1. JOYSTICK SIGNAL PROCESSING ---
            # Standard structural axes mapping
            lx = get_gamepad_axis_movement(gamepad_idx, GAMEPAD_AXIS_LEFT_X)
            ly = get_gamepad_axis_movement(gamepad_idx, GAMEPAD_AXIS_LEFT_Y)
            rx = get_gamepad_axis_movement(gamepad_idx, GAMEPAD_AXIS_RIGHT_X)
            ry = get_gamepad_axis_movement(gamepad_idx, GAMEPAD_AXIS_RIGHT_Y)

            # Left Joystick Tracking UI
            draw_text("Left Analog Stick", 50, 95, 15, BLACK)
            draw_rectangle_lines(50, 120, 100, 100, LIGHTGRAY)
            draw_line(50, 170, 150, 170, LIGHTGRAY) 
            draw_line(100, 120, 100, 220, LIGHTGRAY) 
            draw_circle(int(100 + (lx * 50)), int(170 + (ly * 50)), 6, BLUE)
            draw_text(f"X: {lx:+.2f}\nY: {ly:+.2f}", 50, 230, 12, DARKGRAY)

            # Right Joystick Tracking UI
            draw_text("Right Analog Stick", 220, 95, 15, BLACK)
            draw_rectangle_lines(220, 120, 100, 100, LIGHTGRAY)
            draw_line(220, 170, 320, 170, LIGHTGRAY)
            draw_line(270, 120, 270, 220, LIGHTGRAY)
            draw_circle(int(270 + (rx * 50)), int(170 + (ry * 50)), 6, DARKBLUE)
            draw_text(f"X: {rx:+.2f}\nY: {ry:+.2f}", 220, 230, 12, DARKGRAY)

            # --- 2. ANALOG L2 / R2 DEVIATION ---
            l_trigger = get_gamepad_axis_movement(gamepad_idx, GAMEPAD_AXIS_LEFT_TRIGGER)
            r_trigger = get_gamepad_axis_movement(gamepad_idx, GAMEPAD_AXIS_RIGHT_TRIGGER)

            draw_text("Analog Pressure Triggers", 50, 280, 15, BLACK)
            draw_text(f"L2 Value: {l_trigger:+.2f}", 50, 305, 13, DARKGRAY)
            draw_text(f"R2 Value: {r_trigger:+.2f}", 220, 305, 13, DARKGRAY)

            # --- 3. DIGITAL MATRIX STATE MONITOR ---
            draw_text("Digital Matrix Signals", 450, 95, 16, BLACK)
            
            y_offset = 125
            for name, button_id in buttons:
                is_pressed = is_gamepad_button_down(gamepad_idx, button_id)
                
                # Active elements illuminate in bright green
                indicator_color = GREEN if is_pressed else LIGHTGRAY
                text_color = BLACK if is_pressed else GRAY
                
                draw_rectangle(450, y_offset, 14, 14, indicator_color)
                draw_text(name, 475, y_offset, 13, text_color)
                y_offset += 24

        else:
            draw_text("Gamepad Status: DISCONNECTED", 30, 20, 20, RED)
            draw_text("Please plugin or sync your DualShock 4 device via Bluetooth.", 30, 50, 15, DARKGRAY)

        end_drawing()

    close_window()

if __name__ == "__main__":
    main()
