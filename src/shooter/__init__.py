from pyray import *
import math

class PlayerData:

    def __init__(self, x: float, y: float, angle: float, tex_file: str, name: str):
        self.x = x
        self.y = y
        self.angle = angle
        self.texture = load_texture(tex_file)
        self.width = self.texture.width
        self.height = self.texture.height
        self.name = name

    def __del__(self):
        # This acts as the destructor
        unload_texture(self.texture)

    def draw(self, tint_color: Color):
        draw_texture_pro(self.texture,
                         (0, 0, self.width, self.height),
                         (self.x + self.width/2, self.y + self.height/2, self.width, self.height),
                         (self.width/2, self.height/2),
                         self.angle,
                         tint_color)

def main() -> None:

    # Window initialization
#    set_config_flags(ConfigFlags.FLAG_FULLSCREEN_MODE)
    init_window(1024, 768, "Rocket")

    set_target_fps(60)

    # Players init
    player1 = PlayerData(0, 0, 0, "assets/player1.png", "Oliwier")
    player1.y = float(get_screen_height() - player1.height)

    player2 = PlayerData(0, 0, 0, "assets/player2.png", "Olaf")
    player2.x = float(get_screen_width() - player2.width)
    player2.y = float(get_screen_height() - player2.height)

    # Load textures from PNG files
    # NOTE: Textures must always be loaded AFTER init_window()
    bg_texture = load_texture("assets/background.png")

    # Music and sound
    init_audio_device()
    bg_music = load_music_stream("assets/music.mp3")
    play_music_stream(bg_music)
    explosion = load_sound("assets/explosion.mp3")
    explosion_playing = False

    # Main Game Loop
    while not window_should_close():

        # Movement speed
        speed =  300 * get_frame_time()
    
        # --- 1. KEYBOARD INPUT & MOVEMENT ---
        
        # Left player controls (W, A, S, D)
        if is_key_down(KEY_W): 
            player1.y -= speed
            player1.y = max(player1.y, 0)

        if is_key_down(KEY_S):
            player1.y += speed
            player1.y = min(player1.y, get_screen_height() - player1.height)
        if is_key_down(KEY_A):
            player1.x -= speed
            player1.x = max(player1.x, 0)
        if is_key_down(KEY_D):
            player1.x += speed
            player1.x = min(player1.x, get_screen_width() - player1.width)
        
        # Right Sprite Controls (Arrow Keys)
        if is_key_down(KEY_UP):
            pass
        if is_key_down(KEY_DOWN):
            pass
        if is_key_down(KEY_LEFT):
            player2.angle -= speed
            if player2.angle < 0:
                player2.angle += 360
        if is_key_down(KEY_RIGHT):
            player2.angle += speed
            if player2.angle > 360:
                player2.angle = 0

        player2.x += math.sin(math.radians(player2.angle)) * speed
        player2.x = max(player2.x, 0)
        player2.x = min(player2.x, get_screen_width() - player2.width)

        player2.y -= math.cos(math.radians(player2.angle)) * speed
        player2.y = max(player2.y, 0)
        player2.y = min(player2.y, get_screen_height() - player2.height)

        # --- 2. COLLISION DETECTION ---
        # Check if the two bounding rectangles overlap
        rec1 = Rectangle(player1.x, player1.y, player1.width, player1.height)
        rec2 = Rectangle(player2.x, player2.y, player2.width, player2.height)
        is_colliding = check_collision_recs(rec1, rec2)
        
        # Determine tint color based on collision status
        # Raylib overlays tints: WHITE leaves asset normal; RED filters it completely red
        if is_colliding:
            tint_color = RED
        else:
            tint_color = WHITE

        update_music_stream(bg_music)



        # --- 3. RENDERING ---
        begin_drawing()
        clear_background(RAYWHITE)

        # Draw background
        draw_texture_pro(bg_texture,
                         (0.0, 0.0, bg_texture.width, bg_texture.height),
                         (0, 0, get_screen_width(), get_screen_height()),
                         vector2_zero(),
                         0,
                         WHITE)
        
        # Draw instructions on the screen
        draw_text(f"{player1.name} (Left): W, A, S, D", 10, 10, 20, DARKGRAY)
        t = player2.name + " (Right): Arrow Keys"
        text_size = measure_text(t, 20)
        draw_text(t, get_screen_width() - text_size - 10, 10, 20, DARKGRAY)

        draw_fps(10, 50)

        if is_colliding:
            if not explosion_playing:
                play_sound(explosion)  # Plays the sound effect
                explosion_playing = True
    
            t = "COLLISION DETECTED!"
            text_size = measure_text(t, 24)
            draw_text(t, int((get_screen_width() - text_size)/2), 50, 24, RED)
        else:
            explosion_playing = False
            
        # Draw players at their bounding box X and Y positions with the dynamic tint
        player1.draw(tint_color)
        player2.draw(tint_color)
        
        end_drawing()

    # --- 4. CLEAN UP VRAM & RAM ---
    unload_texture(bg_texture)
    unload_sound(explosion)       # Free memory allocated for the sound
    unload_music_stream(bg_music)
    close_audio_device()       # Shut down the audio engine
    close_window()

if __name__ == '__main__':
    main()
