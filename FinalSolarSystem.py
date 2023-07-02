import numpy as np
import pygame


pygame.init() #initialize pygame

#Window Size
WINDOW_WIDTH = 700 
WINDOW_HEIGHT = 600

pygame.display.set_caption("Solar System")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def getCircle(N, radius=1): #For the vertices of the shapes of planets and sun, and the moon. its actually a polygon but I wrote circle cause i want it to look like a circle 
    v = np.zeros((N, 2)) #We want an initial of (0,0). So we turn everything to zero at the beginning.
    for i in range(N): #Calculate the coordinates for each point on the circle
        angle = i * 360. / N #Calculated by multiplying i with 360. / N. To evenly distribute the points along the circumference of the circle.
        radian = np.deg2rad(angle) #Convert degree to radians

        #return the corresponding x and y values on the unit circle.
        x = radius * np.cos(radian) 
        y = radius * np.sin(radian)

        #stores the coordinates of each point on the circle
        v[i] = [x, y]

    return v

def Rmat(degree): #Generates a 3x3 rotation matrix representing a rotation in 2D space
    radian = np.deg2rad(degree) # trigonometric functions in NumPy work with radians so we convert degrees to radians
    #coefficients of the rotation matrix. just assigned to  variable
    c = np.cos(radian)
    s = np.sin(radian)

    R = np.array([[c, -s, 0], #transformed x-axis after rotation
                  [s, c, 0], #represents the transformed y-axis
                  [0, 0, 1]], dtype='float') #represents the unchanged z-axis (in 2D space). dtype = 'float' to have a more precise position
    return R

def Tmat(tx, ty):
    T = np.array([[1, 0, tx], #rotation
                  [0, 1, ty], #scaling 
                  [0, 0, 1]], dtype='float') #translation component
    return T


#Load image of spaceship
spaceship_img = pygame.image.load("spaceship.png") 
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50)) #resizes the size of the image to a smaller size.

#random x and y
spaceship_x = np.random.randint(0, WINDOW_WIDTH - spaceship_img.get_width()) #By subtracting the spaceship image width from the window width, it ensures that the spaceship stays within the visible area of the window without going off-screen horizontally.
spaceship_y = np.random.randint(0, WINDOW_HEIGHT - spaceship_img.get_height()) #By subtracting the spaceship image width from the window width, it ensures that the spaceship stays within the visible area of the window without going off-screen vertically.

#speed of the movement os the spaceship
spaceship_dx = 1
spaceship_dy = 1

#function draw to draw the shape
#M = transformation matrix that defines the position, rotation, and scaling of the shape
#points = an array of vertices that define the shape to be drawn
#color = default color
#p0 = reference point that is used to draw a line from p0 to the first transformed vertex. If not provided, no line is drawn.
def draw(M, points, color=(0, 0, 0), p0=None):
    R = M[0:2, 0:2] #R represents the rotation and scaling component of the transformation.
    t = M[0:2, 2] # t represents the translation component of the transformation.

    points_transformed = (R @ points.T).T + t #points_transformed variable holds the new coordinates of the vertices in the transformed space.
    pygame.draw.polygon(screen, color, points_transformed) #drawn as a polygon on the screen using the pygame.draw.polygon function, with the specified color.
    if p0 is not None:
        pygame.draw.line(screen, (0, 0, 0), p0, points_transformed[0])

def draw_orbit(center, radius):
    pygame.draw.circle(screen, (50, 50, 50), center, radius, 1) #draw the orbit circle



##########################################################
#Now for the variables we will use for the rotaion

#Sun
angle = 0 # inital value of the sun on its place
Sun = getCircle(100, 25) #using the function above, we draw the circle, 100 is the number of vertices and 25 is the radius

#Mercury
angleSMerc = 0 #Angle of Mercury relative to the sun
distSM = 75 #Distance between sun and mars
Mercury = getCircle(100, 7)  #Circle attributes of mercury
angleM = 0 #inital value for the rotation in its place

#Venus
angleMVenus = 0 #Angle of Venus relative to Mercury
distMV = 50 #distance of Venus to Mercury
Venus = getCircle(100, 10)  # Venus circle attributes
angleV = 0 #initial value for the rotation in ints place

#Earth
angleVEarth = 0 #Angle of earth relative to venus
distVE = 50 #distance of earth to venus
Earth = getCircle(100, 15)  #earth circle attributes
angleE = 0 #initial value for the rotation in its place

#Earth's Moon
angleEMoon = 0 #angle of Earth'sMoon relative to earth
distEM = 30 #distance between them
Moon = getCircle(100, 5)  # Moon circle attributes
angleMoon = 0 #inital moon value for the rotation in its place

#Mars
angleEMars = 0 #angle of mars relative to earth
distEMar = 50 #distance of mars to earth
Mars = getCircle(100, 15)  # Mars circle attributes
angleMrs = 0 #initial value for the rotation in its place

# Moons of Mars
Moon1_Mars = getCircle(100, 5)  # Moon 1 of Mars
Moon2_Mars = getCircle(100, 5)  # Moon 2 of Mars

distMoon1_Mars = 25 # Distance between Mars and Moon 1
distMoon2_Mars = -30  # Distance between Mars and Moon 2

angleMoon1_Mars = 0 #initial value for the rotation in its place
angleMoon2_Mars = 0 #initial value for the rotation in its place


finished = False
while not finished: #Change the angles to different values
    #For its rotation in ints place while revolving the sun
    angle += 1 #for sun in its place
    angleM +=1.5
    angleV += 2
    angleE += 5
    angleMoon += 10
    angleMrs +=3
    angleMoon1_Mars +=  5
    angleMoon2_Mars += 5

    #For its revolution around the sun
    #depending on its distance between the sun, I made the nearer ones faster
    angleSMerc += 1 
    angleMVenus += 0.9 
    angleVEarth += 0.8
    angleEMoon +=1
    angleEMars +=0.7
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    #current coordinates +=  amount by which the spaceship's position changes in the x and y directions, respectively, in each frame.
    #update the spaceship's position
    spaceship_x += spaceship_dx
    spaceship_y += spaceship_dy
    
    #check if the spaceship's position exceeds the window boundaries
    if spaceship_x <= 0 or spaceship_x >= WINDOW_WIDTH - spaceship_img.get_width():
        spaceship_dx *= -1 #if it hits sides, the spaceship moves in the opposite direction horizontally
    if spaceship_y <= 0 or spaceship_y >= WINDOW_HEIGHT - spaceship_img.get_height():
        spaceship_dy *= -1 #if it hits the ceiling or floor,the spaceship moves in the opposite direction vertically

    screen.fill((0)) #fill screen with black color
    screen.blit(spaceship_img, (spaceship_x, spaceship_y)) #showe the spaceship roaming around




    center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2) #center of the screen


    #combines translation (Tmat) and rotation (Rmat) transformations to create a transformation matrix Msun
    #represents the position and orientation of the Sun object in the scene. It translates the Sun to the center coordinates and rotates it by the angle degrees.
    Msun = Tmat(center[0], center[1]) @ Rmat(angle) 
    draw(Msun, Sun, (255, 255, 100), center) #It passes Msun as the transformation matrix then draws the sun with a yellow color
   

    Mmercury = Tmat(center[0], center[1]) @ Rmat(angleSMerc) @ Tmat(distSM, 0) @ Rmat(-angleSMerc) @ Rmat(angleM)
    #Tmat(center[0], center[1]) = translation matrix that moves the coordinate system to the center of the screen. It ensures that Mercury's position is relative to the center.
    #@ Rmat(angleSMerc): This rotates the Mmercury matrix by the angleSMerc degrees around the Z-axis. It represents the orbital rotation of Mercury around the Sun.
    #@ Tmat(distSM, 0): This translates the Mmercury matrix along the X-axis by distSM units. It sets the distance of Mercury from the Sun along its orbit.
    #@ Rmat(-angleSMerc): This rotates the Mmercury matrix in the reverse direction by the -angleSMerc degrees. It compensates for the orbital rotation to ensure that Mercury maintains its orientation.
    #@ Rmat(angleM): This rotates the Mmercury matrix by the angleM degrees around the Z-axis. It represents the rotation of Mercury around its own axis.

    draw(Mmercury, Mercury, (102,153,204), Mmercury[:2, 2])
    #By multiplying the matrices with @, the code calculatrs the final transfomation matrix. that calculates the shape of mercury in the screen coordinates

    draw_orbit(center, distSM) #Draw an orbit

    #So for the rest of the planets are the same, just have a different angles for th rotation on its place, distance from the neighbor planet, and the speed for it to go around the sun

    Mvenus = Tmat(center[0], center[1]) @ Rmat(angleMVenus) @ Tmat(distSM+distMV , 0) @ Rmat(-angleMVenus) @ Rmat(angleV)
    draw(Mvenus, Venus, (196, 164, 132), Mvenus[:2, 2])
    draw_orbit(center, distSM + distMV)

    Mearth = Tmat(center[0], center[1]) @ Rmat(angleVEarth) @ Tmat(distSM + distMV + distVE, 0) @ Rmat(-angleVEarth) @ Rmat(angleE)
    draw(Mearth, Earth, (0,0,255), Mearth[:2, 2])
    draw_orbit(center, distSM + distMV + distVE)

    Mmoon = Mearth @ Rmat(angleEMoon) @ Tmat(distEM, 0) @ Rmat(angleMoon) #to make it revolve around the earth, distance from earth and moon, angle of the rotation of moon in its place
    draw(Mmoon, Moon, (255, 255, 255), Mmoon[:2, 2])
    #Mmoon = ransformation matrix that represents the position and orientation of the Moon.
    #Moon = shape of the Moon, which is typically a set of vertices or points that define its outline.
    #Mmoon[:2, 2]: This expression extracts the translation vector from the Mmoon matrix. 
    # It represents the position of the Moon in the screen coordinates. 
    # The [:2, 2] indexing selects the first two rows (corresponding to X and Y coordinates) and the third column (corresponding to the translation vector).


    Mmars = Tmat(center[0], center[1]) @ Rmat(angleEMars) @ Tmat(distSM + distMV + distVE + distEMar, 0) @ Rmat(-angleEMars) @ Rmat(angleMrs)
    draw(Mmars, Mars, (255,0,0), Mmars[:2, 2])
    draw_orbit(center, distSM + distMV + distVE + distEMar)

    # Same explanation as the Earth's moon
    Mmoon1_Mars = Mmars @ Rmat(angleMoon1_Mars) @ Tmat(distMoon1_Mars, 0) @ Rmat(angleMoon1_Mars)
    draw(Mmoon1_Mars, Moon1_Mars, (255, 255, 255), Mmoon1_Mars[:2, 2])
    Mmoon2_Mars = Mmars @ Rmat(angleMoon2_Mars) @ Tmat(distMoon2_Mars, 0) @ Rmat(angleMoon2_Mars)
    draw(Mmoon2_Mars, Moon2_Mars, (255, 255, 255), Mmoon2_Mars[:2, 2])
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
