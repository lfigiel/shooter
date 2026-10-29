from pyray import *
import math
import sys

SPEED = 200
BULLET_DAMAGE = 5

class Player:

    def __init__(self, x: float, y: float, angle: float, tex_file: str, name: str):
        self.x = x
        self.y = y
        self.angle = angle
        self.texture = load_texture(tex_file)
        self.width = self.texture.width
        self.height = self.texture.height
        self.name = name
        self.health = 100
        self.hit = False
        self.hit_timer = 0
        self.tint_color = WHITE

    def __del__(self):
        # This acts as the destructor
        unload_texture(self.texture)

    def draw(self):
        draw_texture_pro(self.texture,
                         (0, 0, self.width, self.height),
                         (self.x + self.width/2, self.y + self.height/2, self.width, self.height),
                         (self.width/2, self.height/2),
                         self.angle,
                         self.tint_color)

class Bullet:
    def __init__(self, x, y, angle, shooter):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.radius = 5
        self.damage = BULLET_DAMAGE
        self.shooter = shooter
        self.is_alive = True  # Flag to handle collision-based death

    def update(self):
        # Move the bullet upward
        self.x += math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

    def draw(self):
        draw_circle(int(self.x), int(self.y), self.radius, RED)

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
        self.players = []
        self.players.append(Player(0, 0, 0, "assets/ship1.png", self.player1_name))
        self.players[0].y = float(get_screen_height() - self.players[0].height)

        self.players.append(Player(0, 0, 0, "assets/ship2.png", self.player2_name))
        self.players[1].x = float(get_screen_width() - self.players[1].width)
        self.players[1].y = float(get_screen_height() - self.players[1].height)

        # Background
        self.bg_texture = load_texture("assets/background.png")

        # Bullets
        self.bullets = []

        # Music and sound
        init_audio_device()
        self.bg_music = load_music_stream("assets/music.mp3")
        play_music_stream(self.bg_music)
        self.explosion = load_sound("assets/explosion.mp3")
        self.shot = load_sound("assets/shot.mp3")
        self.game_over = False
        self.play = True

    def input(self):
        # --- 1. KEYBOARD INPUT & MOVEMENT ---

        if self.game_over:
            if is_key_pressed(KEY_SPACE): 
                self.play = False
            return

        # player1 controls (W, A, S, D)
        if is_key_down(KEY_W): 
            pass
        if is_key_down(KEY_S):
            pass
        if is_key_down(KEY_A):
            self.players[0].angle -= self.speed
            if self.players[0].angle < 0:
                self.players[0].angle += 360
        if is_key_down(KEY_D):
            self.players[0].angle += self.speed
            if self.players[0].angle > 360:
                self.players[0].angle = 0

        # Add bullet when player shoots
        if is_key_pressed(KEY_LEFT_ALT):
            self.bullets.append(Bullet(self.players[0].x + self.players[0].width/2,
                                       self.players[0].y + self.players[0].height/2,
                                       self.players[0].angle,
                                       0))
            play_sound(self.shot)  # Plays the sound effect


        # player2 controls (Arrow Keys)
        if is_key_down(KEY_UP):
            pass
        if is_key_down(KEY_DOWN):
            pass
        if is_key_down(KEY_LEFT):
            self.players[1].angle -= self.speed
            if self.players[1].angle < 0:
                self.players[1].angle += 360
        if is_key_down(KEY_RIGHT):
            self.players[1].angle += self.speed
            if self.players[1].angle > 360:
                self.players[1].angle = 0

        # Add bullet when player shoots
        if is_key_pressed(KEY_RIGHT_ALT):
            self.bullets.append(Bullet(self.players[1].x + self.players[1].width/2,
                                       self.players[1].y + self.players[1].height/2,
                                       self.players[1].angle,
                                       1))
            play_sound(self.shot)  # Plays the sound effect

    def process(self):
        if self.game_over:
            return

        self.players[0].x += math.sin(math.radians(self.players[0].angle)) * self.speed
        self.players[0].x = max(self.players[0].x, 0)
        self.players[0].x = min(self.players[0].x, get_screen_width() - self.players[0].width)

        self.players[0].y -= math.cos(math.radians(self.players[0].angle)) * self.speed
        self.players[0].y = max(self.players[0].y, 0)
        self.players[0].y = min(self.players[0].y, get_screen_height() - self.players[0].height)

        self.players[1].x += math.sin(math.radians(self.players[1].angle)) * self.speed
        self.players[1].x = max(self.players[1].x, 0)
        self.players[1].x = min(self.players[1].x, get_screen_width() - self.players[1].width)

        self.players[1].y -= math.cos(math.radians(self.players[1].angle)) * self.speed
        self.players[1].y = max(self.players[1].y, 0)
        self.players[1].y = min(self.players[1].y, get_screen_height() - self.players[1].height)

        # --- 2. COLLISION DETECTION ---
        # Check if the two bounding rectangles overlap
        rec1 = Rectangle(self.players[0].x, self.players[0].y, self.players[0].width, self.players[0].height)
        rec2 = Rectangle(self.players[1].x, self.players[1].y, self.players[1].width, self.players[1].height)

        if check_collision_recs(rec1, rec2):
            if not self.is_colliding:
                play_sound(self.explosion)  # Plays the sound effect
                self.is_colliding = True
        else:
            self.is_colliding = False

        # Determine tint color based on collision or hit status
        # Raylib overlays tints: WHITE leaves asset normal; RED filters it completely red
        for player in self.players:
            if self.is_colliding or player.hit:
                player.tint_color = RED
            else:
                player.tint_color = WHITE

            if player.hit and player.hit_timer <= get_time():
                player.hit = False

        # 2. UPDATE: Move and update logic for all bullets
        for bullet in self.bullets:
            bullet.update()

            i = 0 #player index
            for player in self.players:
                if bullet.shooter == i:
                    i =+ 1
                    continue
                if check_collision_circle_rec((bullet.x, bullet.y),
                                              float(bullet.radius),
                                              (player.x, player.y,
                                               player.width, player.height)):
                    play_sound(self.explosion)  # Plays the sound effect
                    player.hit_timer = get_time() + 0.1
                    player.hit = True
                    player.health -= bullet.damage
                    if player.health <= 0:
                        player.health = 0
                        self.game_over = True
                    bullet.is_alive = False
                    continue
                i += 1

            # Check if off-screen (disappearance condition)
            if bullet.x < 0 or bullet.x > get_screen_width() or \
              bullet.y < 0 or bullet.y > get_screen_height():
                bullet.is_alive = False

        # Remove dead/off-screen bullets
        # Rebuilds the list with only active bullets, avoiding mid-loop index errors
        self.bullets = [b for b in self.bullets if b.is_alive]

    def health_color(self, health) -> Color:
        if health <= 20:
            return RED
        else:
            return DARKGRAY

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
        draw_text(f"{self.players[0].name} (Left): W, A, S, D", 10, 10, 20, DARKGRAY)
        draw_text(f"Health: {self.players[0].health}",
                  10,
                  40,
                  20,
                  self.health_color(self.players[0].health))

        t = self.players[1].name + " (Right): Arrow Keys"
        text_size = measure_text(t, 20)
        draw_text(t, get_screen_width() - text_size - 10, 10, 20, DARKGRAY)
        draw_text(f"Health: {self.players[1].health}",
                  get_screen_width() - text_size - 10,
                  40,
                  20,
                  self.health_color(self.players[1].health))

        draw_fps(10, 70)

        if self.game_over:
            t = "GAME OVER"
            text_size = measure_text(t, 40)
            text_y = int(get_screen_height()/2) - 60
            draw_text(t, int((get_screen_width() - text_size)/2), text_y, 40, RED)

            for player in self.players:
                if player.health > 0:
                    t = player.name + " wins !"
                    text_size = measure_text(t, 20)
                    text_y += 60
                    draw_text(t, int((get_screen_width() - text_size)/2), text_y, 20, DARKGRAY)
                    break

            t = "Press SPACE to exit"
            text_size = measure_text(t, 20)
            text_y += 40
            draw_text(t, int((get_screen_width() - text_size)/2), text_y, 20, DARKGRAY)

            end_drawing()
            return

        if self.is_colliding:
            t = "COLLISION DETECTED!"
            text_size = measure_text(t, 24)
            draw_text(t, int((get_screen_width() - text_size)/2), 50, 24, RED)
            
        # Bullets
        for bullet in self.bullets:
            bullet.draw()

        # Draw players at their bounding box X and Y positions with the dynamic tint
        for player in self.players:
            player.draw()


        end_drawing()

    def run(self):

        self.init()

        # Main Game Loop
        while not window_should_close() and self.play:
            # Movement speed
            self.speed =  SPEED * get_frame_time()
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
