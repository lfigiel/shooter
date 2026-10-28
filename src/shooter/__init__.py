from pyray import *
import math
import sys

class Player:

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

class App:

    def __init__(self, args):
        self.player1_name = args[0]
        self.player2_name = args[1]

    def init(self):
        # Window initialization
    #    set_config_flags(ConfigFlags.FLAG_FULLSCREEN_MODE)
        init_window(1024, 768, "Shooter")

        set_target_fps(60)

        # Players init
        self.player1 = Player(0, 0, 0, "assets/ship1.png", self.player1_name)
        self.player1.y = float(get_screen_height() - self.player1.height)

        self.player2 = Player(0, 0, 0, "assets/ship2.png", self.player2_name)
        self.player2.x = float(get_screen_width() - self.player2.width)
        self.player2.y = float(get_screen_height() - self.player2.height)

        # Load textures from PNG files
        # NOTE: Textures must always be loaded AFTER init_window()
        self.bg_texture = load_texture("assets/background.png")

        # Music and sound
        init_audio_device()
        self.bg_music = load_music_stream("assets/music.mp3")
        play_music_stream(self.bg_music)
        self.explosion = load_sound("assets/explosion.mp3")
        self.explosion_playing = False


    def input(self):
        # --- 1. KEYBOARD INPUT & MOVEMENT ---
        
        # player1 controls (W, A, S, D)
        if is_key_down(KEY_W): 
            pass
        if is_key_down(KEY_S):
            pass
        if is_key_down(KEY_A):
            self.player1.angle -= self.speed
            if self.player1.angle < 0:
                self.player1.angle += 360
        if is_key_down(KEY_D):
            self.player1.angle += self.speed
            if self.player1.angle > 360:
                self.player1.angle = 0
        
        # player2 controls (Arrow Keys)
        if is_key_down(KEY_UP):
            pass
        if is_key_down(KEY_DOWN):
            pass
        if is_key_down(KEY_LEFT):
            self.player2.angle -= self.speed
            if self.player2.angle < 0:
                self.player2.angle += 360
        if is_key_down(KEY_RIGHT):
            self.player2.angle += self.speed
            if self.player2.angle > 360:
                self.player2.angle = 0

    def process(self):
        self.player1.x += math.sin(math.radians(self.player1.angle)) * self.speed
        self.player1.x = max(self.player1.x, 0)
        self.player1.x = min(self.player1.x, get_screen_width() - self.player1.width)

        self.player1.y -= math.cos(math.radians(self.player1.angle)) * self.speed
        self.player1.y = max(self.player1.y, 0)
        self.player1.y = min(self.player1.y, get_screen_height() - self.player1.height)

        self.player2.x += math.sin(math.radians(self.player2.angle)) * self.speed
        self.player2.x = max(self.player2.x, 0)
        self.player2.x = min(self.player2.x, get_screen_width() - self.player2.width)

        self.player2.y -= math.cos(math.radians(self.player2.angle)) * self.speed
        self.player2.y = max(self.player2.y, 0)
        self.player2.y = min(self.player2.y, get_screen_height() - self.player2.height)

        # --- 2. COLLISION DETECTION ---
        # Check if the two bounding rectangles overlap
        rec1 = Rectangle(self.player1.x, self.player1.y, self.player1.width, self.player1.height)
        rec2 = Rectangle(self.player2.x, self.player2.y, self.player2.width, self.player2.height)
        self.is_colliding = check_collision_recs(rec1, rec2)
        
        # Determine tint color based on collision status
        # Raylib overlays tints: WHITE leaves asset normal; RED filters it completely red
        if self.is_colliding:
            self.tint_color = RED
        else:
            self.tint_color = WHITE

    def render(self):

        # --- 3. RENDERING ---
        begin_drawing()
        clear_background(RAYWHITE)

        # Draw background
        draw_texture_pro(self.bg_texture,
                        (0.0, 0.0, self.bg_texture.width, self.bg_texture.height),
                        (0, 0, get_screen_width(), get_screen_height()),
                        vector2_zero(),
                        0,
                        WHITE)
        
        # Draw instructions on the screen
        draw_text(f"{self.player1.name} (Left): W, A, S, D", 10, 10, 20, DARKGRAY)
        t = self.player2.name + " (Right): Arrow Keys"
        text_size = measure_text(t, 20)
        draw_text(t, get_screen_width() - text_size - 10, 10, 20, DARKGRAY)

        draw_fps(10, 50)

        if self.is_colliding:
            if not self.explosion_playing:
                play_sound(self.explosion)  # Plays the sound effect
                self.explosion_playing = True
    
            t = "COLLISION DETECTED!"
            text_size = measure_text(t, 24)
            draw_text(t, int((get_screen_width() - text_size)/2), 50, 24, RED)
        else:
            self.explosion_playing = False
            
        # Draw players at their bounding box X and Y positions with the dynamic tint
        self.player1.draw(self.tint_color)
        self.player2.draw(self.tint_color)
        
        end_drawing()


    def run(self):

        self.init()

        # Main Game Loop
        while not window_should_close():
            # Movement speed
            self.speed =  200 * get_frame_time()
            self.input()
            self.process()
            self.render()
            update_music_stream(self.bg_music)

        # --- 4. CLEAN UP VRAM & RAM ---
        unload_texture(self.bg_texture)
        unload_sound(self.explosion)       # Free memory allocated for the sound
        unload_music_stream(self.bg_music)
        close_audio_device()       # Shut down the audio engine
        close_window()

def main() -> None:
    if len(sys.argv) >= 3:
        args = (sys.argv[1], sys.argv[2])
    else:
        args = ("Player1", "Player2")

    app = App(args)
    app.run()

if __name__ == '__main__':
    main()
