import pygame
import numpy as np

pygame.init()
WIDTH = 700
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Arm")
clock = pygame.time.Clock()

def getRegularPolygon(N, radius=1):
    v = np.zeros((N, 2))
    for i in range(N):
        deg = i * 360 / N
        rad = deg * np.pi / 180
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v

def getRectangle(width, height, x=0, y=0):
    points = np.array([[0, 0],
                      [width, 0],
                      [width, height],
                      [0, height]], dtype='float')
    points = points + [x, y]
    return points

   
def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]], dtype='float')
    return R
        
def Tmat(tx, ty):
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]], dtype='float')

    return T

def draw(M, points, color=(0, 0, 0), filled=False):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    transformed_points = np.dot(points, R.T) + t
    pygame.draw.lines(screen, color, True, transformed_points, 3)

#####################################################################
# Variables

Green = (100, 200, 100)
joint_radius = 10
center_radius = 8

center1 = [WIDTH//2, HEIGHT//2]
angle1 = -90  # Initial angle 
width1 = 200
height1 = 30
rect1 = getRectangle(width1, height1)

angle2 = 90  # Initial angle
width2 = 200
height2 = 30
rect2 = getRectangle(width2, height2)

angle3 = 90
width3 = 90
height3 = 30
rect3 = getRectangle(width3, height3)
gap12 = 5

gripper_width = 60
initial_gripper_width = gripper_width
space_pressed = False



#######################################################################
# Loop

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button Pressed!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  
                angle1 += 5
            elif event.key == pygame.K_q:
                angle1 -= 5
            elif event.key == pygame.K_s:
                angle2 += 5
            elif event.key == pygame.K_w:
                angle2 -= 5
            elif event.key == pygame.K_d:
                angle3 += 5
            elif event.key == pygame.K_e:
                angle3 -= 5
            elif event.key == pygame.K_SPACE:
                space_pressed = not space_pressed
                if space_pressed:
                    gripper_width = 30
                else:
                    gripper_width = initial_gripper_width

    screen.fill((0))

    # Draw the Robot

    M1 = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.)
    draw(M1, rect1, (0, 150, 255)) #Draw the first rectangle

    C = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.)
    center2 = C[0:2, 2] #center2
    #draw the circle later to make it above the two rectangles
  
    M2 = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Tmat(gap12, 0) @ Rmat(angle2) @ Tmat(0, -height1/2)
    draw(M2, rect2, (0, 150, 255)) #draw rect2

    C2 = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.)
    center3 = C2[0:2, 2]

    M3 = M2 @ Tmat(width2, 0) @ Tmat(0, height2/2.) @ Tmat(gap12, 0) @ Rmat(angle3) @ Tmat(0, -height2/2.)
    draw(M3, rect3, (0, 150, 255))

    C3 = M2 @ Tmat(width2, 0) @ Tmat(0, height2/2.)
    center4 = C3[0:2, 2]

    M4 = M3 @ Tmat(width2, 0) @ Tmat(0, height3/2.) @ Tmat(gap12, 0) @ Rmat(angle3) @ Tmat(0, -height3/2.)
    C4 = M3 @ Tmat(width3, 0) @ Tmat(0, height3/2.)
    center5 = C4[0:2, 2]

    # Draw joint circles
    pygame.draw.circle(screen, (252, 15, 192), center2, joint_radius)
    pygame.draw.circle(screen, (252, 15, 192), center4, joint_radius)

      
    # Draw gripper
    line_start = int(center5[0] - gripper_width / 2)
    line_end = int(center5[0] + gripper_width / 2)
    line_y = int(center5[1] + 8)
    line_length = 30  
    line_thickness = 10

    if space_pressed: #Here, when i press spacebar, the color o the gripper also changes to pink
        line_color = (252, 15, 192)  
    else:
        line_color = (0, 150, 255) #Here it goes back to orig color


    ##########################
    #Gripper Shape

    pygame.draw.line(screen, line_color, (line_start, line_y), (line_end, line_y), line_thickness) #base of the gripper

    #Grip lines 
    pygame.draw.line(screen, line_color, (line_start, line_y), (line_start, line_y + line_length), line_thickness)
    pygame.draw.line(screen, line_color, (line_end, line_y), (line_end, line_y + line_length), line_thickness)

    # Draw a circle at the gripper center. That connects the gripper to the robot
    pygame.draw.circle(screen, (252, 15, 192), center5, joint_radius)


    #Body of robot 
    box_width = 300
    box_height = 200
    box_x = center1[0] - box_width // 2 
    box_y = center1[1] + center_radius #so that it is at the end of circle
    pygame.draw.rect(screen, (0, 150, 255), (box_x, box_y, box_width, box_height))

    #The center circle. I added it here so that it will be over the box not below it
    pygame.draw.circle(screen, (252, 15, 192), center1, joint_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
