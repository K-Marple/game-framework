import arcade
import random
import math

WIDTH = 1280
HEIGHT = 720
SPRITE_SCALING = 1.0
MOVEMENT_SPEED = 5
ENEMY_COUNT = 7
ENEMY_SPEED = 3

class MenuView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("Welcome to Space Survivor", WIDTH / 2, HEIGHT / 2, arcade.color.DARK_ORANGE, font_size=50, anchor_x="center")
        arcade.draw_text("Press ENTER to start", WIDTH / 2, HEIGHT / 2 - 100, arcade.color.DARK_ORANGE, font_size=30, anchor_x="center")
        arcade.draw_text("Press G for gameplay", WIDTH / 2, HEIGHT / 2 - 150, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)

        if key == arcade.key.G:
            gameplay = GameplayView()
            self.window.show_view(gameplay)

class GameplayView(arcade.View):
    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")


    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("Gameplay", WIDTH / 2, HEIGHT / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Clark is stuck on an alien spaceship.", WIDTH / 2, HEIGHT / 2 - 75, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Collect keys to help him escape the aliens.", WIDTH / 2, HEIGHT / 2 - 95, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Don't get caught by the aliens or its game over.", WIDTH / 2, HEIGHT / 2 - 115, arcade.color.DARK_ORANGE, font_size=20, anchor_x="center")
        arcade.draw_text("Press BACKSPACE to return to main menu", WIDTH / 2, HEIGHT / 2 - 200, arcade.color.DARK_ORANGE, font_size=16, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.BACKSPACE:
            menu = MenuView()
            self.window.show_view(menu)

class Player(arcade.Sprite):
    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH - 1:
            self.right = WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT - 1:
            self.top = HEIGHT - 1

class Alien(arcade.Sprite):
    def follow_sprite(self, player_sprite):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * ENEMY_SPEED
            self.change_y = math.sin(angle) * ENEMY_SPEED

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.time_taken = 0

        self.key_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.window.score = 0

        self.player_sprite = Player(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", scale=SPRITE_SCALING / 2)

        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        for i in range(5):
            yellowKey = arcade.Sprite(":resources:images/items/keyYellow.png", scale=SPRITE_SCALING / 4)

            yellowKey.center_x = random.randrange(WIDTH - 1)
            yellowKey.center_y = random.randrange(HEIGHT - 1)

            self.key_list.append(yellowKey)

        for j in range(ENEMY_COUNT):
            enemy = Alien(":resources:images/alien/alienBlue_front.png", scale=SPRITE_SCALING / 3)
            enemy.center_x = random.randrange(WIDTH - 1)
            enemy.center_y = random.randrange(HEIGHT - 1)

            self.enemy_list.append(enemy)

    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_MIDNIGHT_BLUE

        self.window.set_mouse_visible(False)

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.key_list.draw()
        self.enemy_list.draw()

        output = f"Score: {self.window.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update_player_speed(self):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_update(self, delta_time):
        self.time_taken += delta_time

        self.key_list.update()
        self.player_list.update(delta_time)

        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite)

        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.key_list)
        kill_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)

        for key in hit_list:
            key.kill()
            self.window.score += 1

        for player in kill_list:
            player.kill()

        if len(self.key_list) == 0:
            game_won_view = GameWonView()
            game_won_view.time_taken = self.time_taken
            self.window.set_mouse_visible(True)
            self.window.show_view(game_won_view)

        if kill_list:
            game_over_view = GameOverView()
            game_over_view.time_taken = self.time_taken
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()

class GameWonView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("Congratulations! You Survived!", x=WIDTH / 2, y=400, color=arcade.color.WHITE, font_size=54, anchor_x="center")
        arcade.draw_text("Play Again? (P)", x=WIDTH / 2, y=300, color=arcade.color.WHITE, font_size=24, anchor_x="center")
        arcade.draw_text("Main Menu (M)", x=WIDTH / 2, y=250, color=arcade.color.WHITE, font_size=24, anchor_x="center")


        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}", WIDTH / 2, 200, arcade.color.WHITE, font_size=15, anchor_x="center")

        output_total = f"Score: {self.window.score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.P:
            game = GameView()
            self.window.show_view(game)

        if key == arcade.key.M:
            menu = MenuView()
            self.window.show_view(menu)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")

    
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, WIDTH, HEIGHT))
        arcade.draw_text("You Died. Game Over.", x=WIDTH / 2, y=400, color=arcade.color.WHITE, font_size=54, anchor_x="center")
        arcade.draw_text("Restart? (R)", x=WIDTH / 2, y=300, color=arcade.color.WHITE, font_size=24, anchor_x="center")
        arcade.draw_text("Main Menu (M)", x=WIDTH / 2, y=250, color=arcade.color.WHITE, font_size=24, anchor_x="center")

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        arcade.draw_text(f"Time taken: {time_taken_formatted}", WIDTH / 2, 200, arcade.color.WHITE, font_size=15, anchor_x="center")

        output_total = f"Score: {self.window.score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.R:
            game = GameView()
            self.window.show_view(game)

        if key == arcade.key.M:
            menu = MenuView()
            self.window.show_view(menu)

def main():
    window = arcade.Window(WIDTH, HEIGHT)
    window.score = 0
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()        
