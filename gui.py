import pygame
import random
import numpy as np

######### SETTINGS #########
LOG = False
SHOW_SENSOR_RANGE = False
SPEED = 69  # pixels per second
TARGETS = 5  # Number of targets
SENSORS = 15  # number of sensors
THRESHOLD_DISTANCE = 200  # Minimum distance between sensors
RANGE = 360 # Sensor range
DIRECTION_CHANGE_INTERVAL = 2.5  # Change direction every 2.5 seconds
RATE = 500 # ms
TEXT_COLOR = (255, 255, 255)
SENSOR_COLOR = (76, 145, 204)
TARGET_COLOR = (195, 124, 63)
RANGE_COLOR = (220, 189, 240)
######### SETTINGS #########

# Initialize pygame
pygame.init()
font = pygame.font.Font(None, 25)

# Set up the screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Create positions
sensors_positions = []
for i in range(SENSORS):
    while True:
        # Generate random position
        x = random.randint(40, screen.get_width() - 40)
        y = random.randint(40, screen.get_height() - 40)
        new_sensor_pos = pygame.Vector2(x, y)
        overlap = any(
            new_sensor_pos.distance_to(existing_pos) < THRESHOLD_DISTANCE
            for existing_pos in sensors_positions
        )
        if not overlap:
            sensors_positions.append(new_sensor_pos)
            break
# Matrix init
sensor_connections = np.zeros((SENSORS,SENSORS))
visibility = np.zeros((SENSORS,TARGETS))

# Update sensor_connections matrix
for i, pos1 in enumerate(sensors_positions):
    for j, pos2 in enumerate(sensors_positions[i+1:], i+1):
        if pos1.distance_to(pos2) <= RANGE:
            sensor_connections[i][j] = 1
            sensor_connections[j][i] = 1

if LOG:
    print("Sensor connections matrix:")
    print(sensor_connections)
    print("Sensor positions:")        
    for i, pos in enumerate(sensors_positions):
        print(f"Sensor {i}: ({round(pos.x)}, {round(pos.y)})")
# Init target positions
target_positions = []
for i in range(TARGETS):
    target_positions.append(
        pygame.Vector2(
            random.randint(40, screen.get_width() - 40),
            random.randint(40, screen.get_height() - 40),
        )
    )
# Initialize random movement direction (including diagonals)
movement_directions = []
for i in range(TARGETS):
    movement_directions.append(
        pygame.Vector2(random.choice([1, 0, -1]), random.choice([1, 0, -1]))
    )

# Initialize timer for direction change
direction_change_timers = [0] * TARGETS

# Create a custom event for getting target positions
PRINT_TARGETS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PRINT_TARGETS_EVENT, RATE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == PRINT_TARGETS_EVENT:
            # Update visibility matrix
            for i,pos_t in enumerate(target_positions):
                for j,pos_s in enumerate(sensors_positions):
                    if pos_t.distance_to(pos_s) <= RANGE:
                        visibility[j][i] = 1      

            if LOG:
                print("Visibility matrix:")
                print(visibility) 
                print("Target positions:")
                for i, pos in enumerate(target_positions):
                    print(f"Target {i}: ({round(pos.x)}, {round(pos.y)})")
    # Fill the screen 
    screen.fill((34, 39, 46))
    # Draw the circles
    for i,pos in enumerate(sensors_positions):
        pygame.draw.circle(screen, SENSOR_COLOR, sensors_positions[i], 15)
        if SHOW_SENSOR_RANGE:
            pygame.draw.circle(screen, RANGE_COLOR, sensors_positions[i], RANGE,width=3)
        
        # Add id to sensors
        text_surface = font.render(str(i), True, TEXT_COLOR)  # White text
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

    for i, pos in enumerate(target_positions):
        pygame.draw.circle(screen, TARGET_COLOR, target_positions[i], 20)
        target_positions[i] += movement_directions[i] * SPEED * dt 
        
        # Add id to targets
        text_surface = font.render(str(i), True, TEXT_COLOR)  # White text
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
        if direction_change_timers[i] >= DIRECTION_CHANGE_INTERVAL:
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
