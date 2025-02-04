print("Loading game_logic.py")
import pygame
import random
import math
from settings import *
from sprites import *
from settings import GREEN, DARK_GREEN

class Game:
    def __init__(self, screen, clock):
        # Store the screen and clock objects
        self.screen = screen
        self.clock = clock
        # Game variables
        self.score = 0
        self.best_score = 0
        self.game_over = False
        self.dragonfly_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.moths = []  # List to store all active moths
        self.max_moths = 1  # Start with 1 moth
        self.bats = []
        self.current_time = 0
        self.last_bat_spawn_time = 0
        self.bat_spawn_timer = 5000  # Initial bat spawn timer
        self.power_up_active = False  # Tracks if the power-up is active
        self.power_up_start_time = 0  # Tracks when the power-up started
        self.power_up_duration = 10000  # Power-up lasts for 10 seconds (in milliseconds)
        self.luminous_dots = []  # List to store the positions of luminous green dots

    def spawn_luminous_dot(self):
        """Spawn a luminous green dot at a random position within the playable area."""
        if len(self.luminous_dots) == 0 and random.random() < 0.02:  # 2% chance per frame to spawn a dot
            new_dot = [
                random.randint(PLAYABLE_OFFSET_X, PLAYABLE_WIDTH + PLAYABLE_OFFSET_X - 10),
                random.randint(PLAYABLE_OFFSET_Y, PLAYABLE_HEIGHT + PLAYABLE_OFFSET_Y - 10)
            ]
            self.luminous_dots.append(new_dot)

    def move_luminous_dot(self):
        """Move the luminous dot away from the dragonfly."""
        if self.luminous_dots:
            dot = self.luminous_dots[0]
            dx = dot[0] - self.dragonfly_position[0]
            dy = dot[1] - self.dragonfly_position[1]
            distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            dot[0] += dx / distance * 2  # Move the dot away slowly
            dot[1] += dy / distance * 2
            # Keep the dot within playable area bounds
            dot[0] = max(PLAYABLE_OFFSET_X, min(dot[0], PLAYABLE_WIDTH + PLAYABLE_OFFSET_X - 10))
            dot[1] = max(PLAYABLE_OFFSET_Y, min(dot[1], PLAYABLE_HEIGHT + PLAYABLE_OFFSET_Y - 10))
                
    def check_power_up_collision(self):
        """Check for collisions between the dragonfly and luminous dots."""
        if self.luminous_dots:  # Check if there is a dot
            dot = self.luminous_dots[0]  
            if (
                self.dragonfly_position[0] < dot[0] + 10 and self.dragonfly_position[0] + 50 > dot[0] and
                self.dragonfly_position[1] < dot[1] + 10 and self.dragonfly_position[1] + 50 > dot[1]
            ):
                self.luminous_dots.clear()  # Remove the dot
                self.activate_power_up()  # Activate the power-up

    def activate_power_up(self):
        """Activate the power-up"""
        self.power_up_active = True
        self.power_up_start_time = pygame.time.get_ticks()

    def deactivate_power_up(self):
        """Deactivate the power-up"""
        self.power_up_active = False

    def check_power_up_timer(self):
        """Check if the power-up duration has expired."""
        if self.power_up_active:
            elapsed_time = pygame.time.get_ticks() - self.power_up_start_time
            if elapsed_time >= self.power_up_duration:
                self.deactivate_power_up()

    def draw_power_up_timer(self):
        """Draw a flashing countdown timer for the power-up."""
        if self.power_up_active:
            remaining_time = max(0, (self.power_up_duration - (pygame.time.get_ticks() - self.power_up_start_time)) // 1000)
            timer_text = font.render(f"Power-Up: {remaining_time}s", True, GREEN if int(pygame.time.get_ticks() / 500) % 2 == 0 else DARK_GREEN)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

    def draw_background(self):
        """Draws the night sky background."""
        self.screen.blit(background_image, (0, 0))

    def calculate_max_moths(self):
        """Calculate the maximum number of moths based on the current score."""
        return max(1, (self.score // 50) + 1)

    def draw_score(self):
        """Draws the score and best score on the screen."""
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        best_score_text = font.render(f"Best Score: {self.best_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(best_score_text, (10, 50))

    def show_reached_score(self):
        """Display the reached score on the screen."""
        reached_score_text = font.render(f"Reached Score: {self.score}", True, WHITE)
        self.screen.blit(reached_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

    def show_best_score(self):
        """Display the best score on the screen."""
        best_score_text = font.render(f"Best Score: {self.best_score}", True, WHITE)
        self.screen.blit(best_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    def reset_game(self):
        """Reset the game state for a new round."""
        self.score = 0
        self.dragonfly_position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.moths = []  # Reset moths
        self.bats = []
        self.current_time = 0
        self.last_bat_spawn_time = 0
        self.bat_spawn_timer = 5000
        self.game_over = False
        # Spawn the first moth immediately
        self.spawn_moth()

    def spawn_moth(self):
        """Spawn a new moth at a random position within the playable area."""
        if len(self.moths) < self.max_moths:  # Only spawn if below the max limit
            new_moth = [
                random.randint(PLAYABLE_OFFSET_X, PLAYABLE_WIDTH + PLAYABLE_OFFSET_X - 30),
                random.randint(PLAYABLE_OFFSET_Y, PLAYABLE_HEIGHT + PLAYABLE_OFFSET_Y - 30)
            ]
            self.moths.append(new_moth)

    def spawn_bat(self):
        """Spawn a new bat at a random position outside the screen."""
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x, y = random.randint(0, SCREEN_WIDTH), -40
        elif side == 'bottom':
            x, y = random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 40
        elif side == 'left':
            x, y = -40, random.randint(0, SCREEN_HEIGHT)
        else:
            x, y = SCREEN_WIDTH + 40, random.randint(0, SCREEN_HEIGHT)
        self.bats.append([x, y, random.randint(3, 6)])  # Bat speed increased to between 3 and 6

    def move_bats(self):
        """Move bats towards the dragonfly."""
        for bat in self.bats:
            dx = self.dragonfly_position[0] - bat[0]
            dy = self.dragonfly_position[1] - bat[1]
            distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            bat[0] += dx / distance * bat[2]
            bat[1] += dy / distance * bat[2]

    def move_moths(self):
        """Move all moths away from the dragonfly within the playable area."""
        for moth in self.moths:
            dx = moth[0] - self.dragonfly_position[0]
            dy = moth[1] - self.dragonfly_position[1]
            distance = max(1, (dx**2 + dy**2)**0.5)  # Avoid division by zero
            moth[0] += dx / distance * 2  # Moth moves away slowly
            moth[1] += dy / distance * 2
            # Keep moth within playable area bounds
            moth[0] = max(PLAYABLE_OFFSET_X, min(moth[0], PLAYABLE_WIDTH + PLAYABLE_OFFSET_X - 30))
            moth[1] = max(PLAYABLE_OFFSET_Y, min(moth[1], PLAYABLE_HEIGHT + PLAYABLE_OFFSET_Y - 30))

    def check_collisions(self):
        """Check for collisions between dragonfly, moths, and bats."""
        # Check collision with moths
        for moth in self.moths[:]:  # Iterate over a copy to allow removal during iteration
            if (
                self.dragonfly_position[0] < moth[0] + 30 and self.dragonfly_position[0] + (100 if self.power_up_active else 50) > moth[0] and
                self.dragonfly_position[1] < moth[1] + 30 and self.dragonfly_position[1] + (100 if self.power_up_active else 50) > moth[1]
            ):
                self.score += 5
                self.moths.remove(moth)  # Remove the eaten moth
                break  # Exit after one collision per frame

        # Check collision with bats
        for bat in self.bats[:]:  # Iterate over a copy to allow removal during iteration
            if self.power_up_active and (
                self.dragonfly_position[0] < bat[0] + 20 and self.dragonfly_position[0] + (100 if self.power_up_active else 50) > bat[0] and
                self.dragonfly_position[1] < bat[1] + 20 and self.dragonfly_position[1] + (100 if self.power_up_active else 50) > bat[1]
            ):
                self.score += 10  # Eating a bat gives more points
                self.bats.remove(bat)  # Remove the eaten bat
                break  # Exit after one collision per frame

        # If not in power-up mode, check for game-over condition
        if not self.power_up_active:
            for bat in self.bats:
                if (
                    self.dragonfly_position[0] < bat[0] + 20 and self.dragonfly_position[0] + 50 > bat[0] and
                    self.dragonfly_position[1] < bat[1] + 20 and self.dragonfly_position[1] + 50 > bat[1]
                ):
                    self.game_over = True

    def rotate_dragonfly(self):
        """Rotate the dragonfly sprite to face the nearest moth."""
        if self.moths:
            target_moth = self.moths[0]  # Use the first moth as the target
            dx = target_moth[0] - self.dragonfly_position[0]
            dy = target_moth[1] - self.dragonfly_position[1]
            angle = math.degrees(math.atan2(-dy, dx))  # Calculate angle to face the moth
            rotated_image = pygame.transform.rotate(dragonfly_image, angle)
            return rotated_image
        return dragonfly_image

    def rotate_bat(self, bat):
        """Rotate the bat sprite to face the dragonfly."""
        dx = self.dragonfly_position[0] - bat[0]
        dy = self.dragonfly_position[1] - bat[1]
        angle = math.degrees(math.atan2(-dy, dx))  # Calculate angle to face the dragonfly
        rotated_image = pygame.transform.rotate(bat_image, angle)
        return rotated_image

    def main(self):
        running = True
        self.reset_game()
        while running:
            self.current_time = pygame.time.get_ticks()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Continuous movement using pygame.key.get_pressed()
            keys = pygame.key.get_pressed()
            if not self.game_over:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.dragonfly_position[0] -= 8  # Move left
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.dragonfly_position[0] += 8  # Move right
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.dragonfly_position[1] -= 8  # Move up
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.dragonfly_position[1] += 8  # Move down

            # Dragonfly wraps around the playable area
            if self.dragonfly_position[0] < PLAYABLE_OFFSET_X - 50:
                self.dragonfly_position[0] = PLAYABLE_WIDTH + PLAYABLE_OFFSET_X
            elif self.dragonfly_position[0] > PLAYABLE_WIDTH + PLAYABLE_OFFSET_X:
                self.dragonfly_position[0] = PLAYABLE_OFFSET_X - 50
            if self.dragonfly_position[1] < PLAYABLE_OFFSET_Y - 50:
                self.dragonfly_position[1] = PLAYABLE_HEIGHT + PLAYABLE_OFFSET_Y
            elif self.dragonfly_position[1] > PLAYABLE_HEIGHT + PLAYABLE_OFFSET_Y:
                self.dragonfly_position[1] = PLAYABLE_OFFSET_Y - 50

            # Update power-up state
            self.check_power_up_timer()

            # Spawn luminous dots
            self.spawn_luminous_dot()

            # Update max moths based on score
            self.max_moths = self.calculate_max_moths()

            # Spawn bats
            if self.current_time - self.last_bat_spawn_time >= self.bat_spawn_timer:
                self.spawn_bat()
                self.last_bat_spawn_time = self.current_time
                self.bat_spawn_timer = 15000  # Subsequent bats spawn every 15 seconds

            # Move bats
            self.move_bats()

            # Move moths
            self.move_moths()

            self.move_luminous_dot()

            # Check collisions
            self.check_power_up_collision()
            self.check_collisions()

            # Spawn new moths if needed
            if len(self.moths) < self.max_moths:
                self.spawn_moth()

            # Draw everything
            self.draw_background()
            rotated_dragonfly = self.rotate_dragonfly()
            dragonfly_rect = rotated_dragonfly.get_rect(center=self.dragonfly_position)
            self.screen.blit(rotated_dragonfly, dragonfly_rect.topleft)

            # Draw moths
            for moth in self.moths:
                self.screen.blit(moth_image, moth)

            # Draw bats
            for bat in self.bats:
                rotated_bat = self.rotate_bat(bat)
                bat_rect = rotated_bat.get_rect(center=(bat[0] + 20, bat[1] + 20))
                self.screen.blit(rotated_bat, bat_rect.topleft)

            # Draw luminous dot
            if self.luminous_dots:
                pygame.draw.circle(self.screen, GREEN, self.luminous_dots[0], 5)

            # Draw power-up timer
            self.draw_power_up_timer()

            # Draw score
            self.draw_score()

            if self.game_over:
                # Game over screen
                self.draw_background()
                self.show_reached_score()
                self.show_best_score()
                pygame.display.flip()

                # Wait for user input after game over
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                                running = False
                                waiting = False
                            elif event.key == pygame.K_SPACE:
                                self.best_score = max(self.best_score, self.score)  # Update best score
                                self.reset_game()  # Reset the game
                                waiting = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()