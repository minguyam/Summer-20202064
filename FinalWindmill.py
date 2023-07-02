import pygame
import numpy as np


pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


pygame.init()
pygame.display.set_caption("Windmill")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

#############################################
def getRectangle(width, height, x=0, y=0): #vertices of a rectangle shape based on the provided width and height
    points = np.array([[0, 0], #top-left corner of the rectangle.
                      [width, 0], # top-right corner of the rectangle.
                      [width, height], #the bottom-right corner of the rectangle.
                      [0, height]], dtype='float') #the bottom-left corner of the rectangle.
    points = points + [x, y] #translates all the vertices of the rectangle by the values of x and y
    return points

def Rmat(degree): #generates a 3x3 rotation matrix representing a rotation in 2D space
    radian = np.deg2rad(degree) #angle in degrees is converted to radians
    #the cosine and sin are set to a  variable 
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0], #transformed x-axis after rotation
                  [s, c, 0], #transformed y-axis
                  [0, 0, 1]], dtype='float') #represents the z-axis in 2D space, #use float for a more precise calcu. more detailed
    return R
        
def Tmat(tx, ty): #3x3 translation matrix representing a translation in 2D space. tx and ty are the translation distances along the x-axis and y-axis
    T = np.array([[1, 0, tx], #no translation along the x-axis.
                  [0, 1, ty], #no translation along the y-axis.
                  [0, 0, 1]], dtype='float') #the translation along the x-axis and y-axis

    return T

def draw(M, points, color=(0, 0, 0), p0=None):
    R = M[0:2, 0:2] #R represents the rotation and scaling component of the transformation.
    t = M[0:2, 2] # t represents the translation component of the transformation.

    points_transformed = (R @ points.T).T + t #points_transformed variable holds the new coordinates of the vertices in the transformed space.
    pygame.draw.polygon(screen, color, points_transformed,5) #drawn as a polygon on the screen using the pygame.draw.polygon function, with the specified color.
    if p0 is not None:
        pygame.draw.line(screen, (0, 0, 0), p0, points_transformed[0])

#################################################
#Rectangle Variables
#Use the getRectangle() function to drawthe rectange
width3 = 150
height3 = 50
rect3 = getRectangle(width3, height3, x=0, y=-height3/2.)


angle = 0 #initial angle

finished = False 
while not finished:
    angle += 3 #the speed of the angle turning +=3 direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        
    screen.fill((0))

    cent = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2) #center of the screen

    M = Tmat(cent[0], cent[1])  #Creates a transformation matrix M by translating the coordinates by cent[0] units along the X-axis and cent[1] units along the Y-axis.
    M1 = M @ Rmat(angle) #Creates a new transformation matrix M1 by combining the transformation matrix M with a rotation matrix Rmat(angle), representing a rotation by the specified angle.
    M2 = M1 @ Rmat(90) #transformation matrix M2 by combining the previous transformation matrix M1 with a rotation matrix Rmat(90), representing a 90-degree rotation.
    M3 = M2 @ Rmat(90) #transformation matrix M3 by combining the previous transformation matrix M2 with another rotation matrix Rmat(90), representing another 90-degree rotation.
    M4 = M3 @ Rmat(90) #final transformation matrix M4 by combining the previous transformation matrix M3 with another rotation matrix Rmat(90), representing another 90-degree rotation.

    #These lines of code call the "draw" function to render the shape `rect3` on the screen using different transformation matrices (`M1`, `M2`, `M3`, `M4`)
    # Each rect isfilled with the neon blue color
    draw(M1, rect3, (0, 150, 255))
    draw(M2, rect3, (0, 150, 255))
    draw(M3, rect3, (0, 150, 255))
    draw(M4, rect3, (0, 150, 255))


    # Draw ground line
    ground_start = (cent[0], cent[1])  #the center of the screen
    ground_end = (cent[0], WINDOW_HEIGHT)  #centerx and the ground
    pygame.draw.line(screen, (0, 150, 255), ground_start, ground_end, 5) #line from center to ground
    pygame.draw.circle(screen, (252, 15, 192), cent, 10) #draw the center circle. I placed it here so that it would not be overlapped by the rectangles
    
   
    pygame.display.flip()
    clock.tick(60)


pygame.quit()