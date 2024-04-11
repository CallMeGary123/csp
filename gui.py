import pygame
import random
LOG = False
# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
targets = 3  # Number of targets
sensors = 9  # number of sensors
threshold_distance = 200  # Minimum distance between sensors
font = pygame.font.Font(None, 25)
# Create target positions
target_positions = []
sensors_positions = []
for i in range(sensors):
    while True:
        # Generate random position
        x = random.randint(40, screen.get_width() - 40)
        y = random.randint(40, screen.get_height() - 40)
        new_sensor_pos = pygame.Vector2(x, y)
        overlap = any(
            new_sensor_pos.distance_to(existing_pos) < threshold_distance
            for existing_pos in sensors_positions
        )

        if not overlap:
            sensors_positions.append(new_sensor_pos)
            break
if LOG:        
    for i, pos in enumerate(sensors_positions):
        print(f"Sensor {i}: ({round(pos.x)}, {round(pos.y)})")
for i in range(targets):
    target_positions.append(
        pygame.Vector2(
            random.randint(40, screen.get_width() - 40),
            random.randint(40, screen.get_height() - 40),
        )
    )
# Initialize random movement direction (including diagonals)
movement_directions = []
for i in range(targets):
    movement_directions.append(
        pygame.Vector2(random.choice([1, 0, -1]), random.choice([1, 0, -1]))
    )

# Initialize timer for direction change
direction_change_timers = [0] * targets
direction_change_interval = 2.5  # Change direction every 2.5 seconds

# Create a custom event for printing target positions
PRINT_TARGETS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PRINT_TARGETS_EVENT, 500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == PRINT_TARGETS_EVENT:
            # Print target positions to the terminal
            if LOG:
                for i, pos in enumerate(target_positions):
                    print(f"Target {i}: ({round(pos.x)}, {round(pos.y)})")
    # Fill the screen with purple
    screen.fill((34, 39, 46))
    # Draw the circles
    for i,pos in enumerate(sensors_positions):
        pygame.draw.circle(screen, (76, 145, 204), sensors_positions[i], 15)
        text_surface = font.render(str(i), True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

    for i, pos in enumerate(target_positions):
        pygame.draw.circle(screen, (195, 124, 63), target_positions[i], 20)
        target_positions[i] += movement_directions[i] * 100 * dt
        text_surface = font.render(str(i), True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)
        # Check if the circle hits the screen edge
        if (
            target_positions[i].x < 40
            or target_positions[i].x > screen.get_width() - 40
        ):
            movement_directions[i].x *= -1  # Reverse x-direction
        if (
            target_positions[i].y < 40
            or target_positions[i].y > screen.get_height() - 40
        ):
            movement_directions[i].y *= -1  # Reverse y-direction
        # Update direction change timer
        direction_change_timers[i] += dt
        if direction_change_timers[i] >= direction_change_interval:
            # Randomize both x and y directions
            movement_directions[i] = pygame.Vector2(
                random.choice([1, 0, -1]), random.choice([1, 0, -1])
            )
            direction_change_timers[i] = 0
    # Update the display
    pygame.display.flip()
    # Limit FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
