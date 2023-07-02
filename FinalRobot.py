import pygame
import numpy as np

pygame.init()
WIDTH = 700
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Arm")
clock = pygame.time.Clock()


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

def draw(M, points, color=(0, 0, 0), filled=False):
    R = M[0:2, 0:2] #extracts the 2x2 submatrix from the transformation matrix
    t = M[0:2, 2] #rotation and scaling component of the transformation

    transformed_points = np.dot(points, R.T) + t #transformation to the set of points that define the shape.
    pygame.draw.lines(screen, color, True, transformed_points, 3) #draws the transformed shape on the screen using the pygame.draw.lines func

#####################################################################
# Variables

joint_radius = 10 #radius for the joints
center_radius = 8 #the radius for the center

center1 = [WIDTH//2, HEIGHT//2] #center of the screen
angle1 = -90  # Initial angle  for the first arm that goes upward. the base arm
width1 = 200 #width of 200 for the rectangle
height1 = 30#height of 30
rect1 = getRectangle(width1, height1) #get the rectangle attributes

#Same as rect1 but only has different values
angle2 = 90  
width2 = 200
height2 = 30
rect2 = getRectangle(width2, height2)

angle3 = 90
width3 = 90
height3 = 30
rect3 = getRectangle(width3, height3)

gap12 = 5#gap between the rectangles

#gripper
gripper_width = 60 #nitial width
initial_gripper_width = gripper_width
space_pressed = False #not yet gripped



#######################################################################
# Loop

finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:  
                angle1 += 5 #for the first arm. move forward clockwise +5
            elif event.key == pygame.K_q:
                angle1 -= 5 #first arm. move backwardcounterclockwise
            elif event.key == pygame.K_s:
                angle2 += 5 #second arm, forwardclockwise
            elif event.key == pygame.K_w:
                angle2 -= 5 #second arm, backwardcounterclockwise
            elif event.key == pygame.K_d:
                angle3 += 5 #third arm, forward clockwise
            elif event.key == pygame.K_e:
                angle3 -= 5 #third arm, backward, counterclockwise
            elif event.key == pygame.K_SPACE:
                space_pressed = not space_pressed  #if turns true
                if space_pressed:
                    gripper_width = 30 #gripper width becomes 30. kind of like gripping something
                else:
                    gripper_width = initial_gripper_width
                    #goes back to normal

    screen.fill((0))

    # Draw the Robot

    #transformation matrix M1 by combining translation and rotation transformations.
    #np.eye = identity matrix 
    #Tmat(center1[0], center1[1])= translation to move the origin to center1 coordinates
    #Rmat(angle1) =  to rotate the coordinate system by angle1 degrees.
    #Tmat(0, -height1/2.) = another translation to adjust the position of the rectangle
    M1 = np.eye(3) @ Tmat(center1[0], center1[1]) @ Rmat(angle1) @ Tmat(0, -height1/2.) 
    draw(M1, rect1, (0, 150, 255)) #Draw the first rectangle using the M1 transformation matrix

    #M1 = initial transformation matrix
    #Tmat(width1, 0) translates the coordinate system by width1 units along the X-axis.
    #Tmat(0, height1/2.) translates the coordinate system by height1/2. units along the Y-axis.
    C = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.) 
    #center2 = C[0:2, 2] extracts the values from the first two rows ([0:2]) and the third column ([2]
    center2 = C[0:2, 2] #new position of the center point in the transformed coordinate system
    
    #M1 represents the initial transformation matrix obtained from the previous calculations.
    #Tmat(width1, 0) translates the coordinate system by width1 units along the X-axis.
    #Tmat(0, height1/2.) translates the coordinate system by height1/2. units along the Y-axis.
    #Tmat(gap12, 0) translates the coordinate system by gap12 units along the X-axis.
    #Rmat(angle2) rotates the coordinate system by angle2 degrees around the Z-axis.
    #Tmat(0, -height1/2) translates the coordinate system by -height1/2. units along the Y-axis.
    #This goes the same for the rest. Just with a change in some values. They are connected to each other.
    M2 = M1 @ Tmat(width1, 0) @ Tmat(0, height1/2.) @ Tmat(gap12, 0) @ Rmat(angle2) @ Tmat(0, -height1/2)
    draw(M2, rect2, (0, 150, 255)) 

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
    box_x = center1[0] - box_width // 2 #nsures that the body is horizontally centered around center1.
    box_y = center1[1] + center_radius #so that it is at the end of circle
    pygame.draw.rect(screen, (0, 150, 255), (box_x, box_y, box_width, box_height))

    #The center circle. I added it here so that it will be over the box not below it
    pygame.draw.circle(screen, (252, 15, 192), center1, joint_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()