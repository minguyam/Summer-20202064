import pygame
import time
import numpy as np

# Initialize Pygame
pygame.init()

# Window Size
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Bell sound
bell_sound = pygame.mixer.Sound('bell.wav')  # for the bell sound

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Clock")
clock = pygame.time.Clock()

# Transformation Matrix
def Tmat(dx, dy):
    return np.array([[1, 0, dx], #transformation of the X-coordinate
                     [0, 1, dy], #transformation of the Y-coordinate
                     [0, 0, 1]]) #no change in the Z-coordinate

# Rotational Matrix
def Rmat(angle):
    #cos and sin of the angles changes to variables
    c = np.cos(angle) 
    s = np.sin(angle)
    return np.array([[c, -s, 0], # transformation of the X-coordinate
                     [s, c, 0], #transformation of the Y-coordinate
                     [0, 0, 1]]) ##no change in the Z-coordinate
#The cosine and sine functions are used to calculate the new coordinates after rotation.


finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

 
    screen.fill(BLACK)

    
    clock_radius = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2 - 20 
    #calculates the radius for the clock by taking the minimum of the window's width and height, dividing it by 2, and subtracting 20 to provide a margin.
    clock_center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    

    # Draw the clock circle
    pygame.draw.circle(screen, (0, 150, 255), clock_center, clock_radius, 10) #clock itself
    pygame.draw.circle(screen, (252, 15, 192), clock_center, 10) #The center circle where the hands are connected to
  

    font = pygame.font.Font(None, 40) #font dsign. The size

    for i in range(1, 13): #1-12 will be written on the clock
        angle = np.radians((i - 3) * 30)  # shift the angle by 90 degrees to position 12 at the top
        x = int(clock_center[0] + (clock_radius - 60) * np.cos(angle)) #to make sure its inside the circle. written in a circular motion
        y = int(clock_center[1] + (clock_radius - 60) * np.sin(angle)) #to make sure its inside the circle. written in a circular motion
        number_text = font.render(str(i), True, WHITE) #Numbers are written 
        number_rect = number_text.get_rect(center=(x, y))  #obtain the rectangle bounding box for the rendered 
        screen.blit(number_text, number_rect) #number_text is blitted (drawn) onto the screen surface at the location defined by the number_rect rectangle.

    # Get the current time
    current_time = time.localtime()
    hour = current_time.tm_hour % 12  # Convert to 12-hour format
    minute = current_time.tm_min #the min
    second = current_time.tm_sec #the secs

    # Calculate the angle for each hand
    hour_angle = np.radians((hour * 30) - 90) + np.radians((minute / 60) * 30)  # 360 degrees / 12 hours = 30 degrees per hour
    minute_angle = np.radians((minute * 6) - 90)  # 360 degrees / 60 minutes = 6 degrees per minute
    second_angle = np.radians((second + time.time() % 1) * 6 - 90)  # 360 degrees / 60 seconds = 6 degrees per second

    # Length of the hands of the hour, minute, and second hands
    hour_length = 150
    minute_length = 200
    second_length = 200

    # Create transformation matrices
    hour_transform = Tmat(clock_center[0], clock_center[1]) @ Rmat(hour_angle) @ Tmat(hour_length, 0)
    #`hour_transform` is a transformation matrix obtained by translating the origin to the clock center,
    # rotating by the `hour_angle` angle, 
    # and then extending the transformed length by `hour_length` in the X-axis.
    #This goes the same for minute_transform and second_transform as well
    minute_transform = Tmat(clock_center[0], clock_center[1]) @ Rmat(minute_angle) @ Tmat(minute_length, 0)
    second_transform = Tmat(clock_center[0], clock_center[1]) @ Rmat(second_angle) @ Tmat(second_length, 0)

    # Calculate the hand endpoints
    hour_end = hour_transform @ np.array([[0], [0], [1]])
    #calculates the endpoint of the hour hand by multiplying the transformation matrix hour_transform with the origin point [0, 0, 1] 
    # to obtain the transformed coordinates [x, y, 1].
    #same for the minute and second endpoints
    minute_end = minute_transform @ np.array([[0], [0], [1]])
    second_end = second_transform @ np.array([[0], [0], [1]])

    # Draw the clock hands
    #For all three goes the same
    #draws a line on the screen from the clock center to the calculated endpoint of the hour hand, 
    #using the color (252, 15, 192) and a line thickness of 8 pixels.
    pygame.draw.line(screen, (252, 15, 192), clock_center, (hour_end[0, 0], hour_end[1, 0]), 8)
    pygame.draw.line(screen, (252, 15, 192), clock_center, (minute_end[0, 0], minute_end[1, 0]), 5)
    pygame.draw.line(screen, (252, 15, 192), clock_center, (second_end[0, 0], second_end[1, 0]), 2)

    # Play bell sound at every hour
    if minute == 0 and second == 0:
        bell_sound.play()

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
