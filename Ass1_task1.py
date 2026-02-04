#task1###############################################
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Global Var
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 300

# Rain var
rain_drops = []
rain_direction = 0.0  # 0 means straight down
rain_speed = 8.0
MAX_RAIN_DROPS = 100

# Day/Night 
background_color = [0.0, 0.0, 1.0]  # Initialize with light blue(day) but after day_night_factor call from animation,start with dark blue (night)
day_night_factor = 0.0  # night = 0, day = 1

# House position and size
house_x, house_y = 0, -180
house_width, house_height = 200, 150

# Rain fun
def init_rain():
    global rain_drops
    rain_drops = []
    for i in range(MAX_RAIN_DROPS):
        x = random.uniform(-400, 400)
        y = random.uniform(-300, 300)
        speed = random.uniform(rain_speed * 0.8, rain_speed * 1.2)
        rain_drops.append([x, y, speed])

# Draw Connected Triangular Bushes 
def draw_connected_bushes():
    bush_color = 0.3 - 0.1 * day_night_factor  
    glColor3f(0.1, bush_color, 0.1)
    
    # Draw continuous connected triangles from left to right
    start_x = -400
    end_x = 400
    triangle_width = 60  # Width of each triangle base
    triangle_height = 40  # Height of each triangle
    
    current_x = start_x
    
    while current_x < end_x:
        # Draw one triangle
        glBegin(GL_TRIANGLES)
        glVertex2f(current_x, -180)  # Left base point
        glVertex2f(current_x + triangle_width, -180)  # Right base point
        glVertex2f(current_x + triangle_width/2, -180 + triangle_height)  # Top point
        glEnd()
        
        # Move to next position (connected - right base becomes left base of next triangle)
        current_x += triangle_width

# Draw House
def draw_house():
    # Main house body (two triangles)
    glColor3f(0.7, 0.5, 0.3)  
    glBegin(GL_TRIANGLES)
    # First triangle of rectangle
    glVertex2f(house_x - house_width/2, house_y)
    glVertex2f(house_x + house_width/2, house_y)
    glVertex2f(house_x - house_width/2, house_y + house_height)
    # Second triangle of rectangle
    glVertex2f(house_x + house_width/2, house_y)
    glVertex2f(house_x + house_width/2, house_y + house_height)
    glVertex2f(house_x - house_width/2, house_y + house_height)
    glEnd()
    
    # Roof (triangle)
    glColor3f(0.5, 0.2, 0.1)  
    glBegin(GL_TRIANGLES)
    glVertex2f(house_x - house_width/2 - 10, house_y + house_height)
    glVertex2f(house_x + house_width/2 + 10, house_y + house_height)
    glVertex2f(house_x, house_y + house_height + 80)
    glEnd()
    
    # Door (rectangle, so two triangles)
    glColor3f(0.3, 0.2, 0.1)  
    glBegin(GL_TRIANGLES)
    door_width = 40
    door_height = 70
    # First triangle of door
    glVertex2f(house_x - door_width/2, house_y)
    glVertex2f(house_x + door_width/2, house_y)
    glVertex2f(house_x - door_width/2, house_y + door_height)
    # Second triangle of door
    glVertex2f(house_x + door_width/2, house_y)
    glVertex2f(house_x + door_width/2, house_y + door_height)
    glVertex2f(house_x - door_width/2, house_y + door_height)
    glEnd()
    
    # Door handle point
    glColor3f(0.9, 0.9, 0.2)  
    glPointSize(6)
    glBegin(GL_POINTS)
    glVertex2f(house_x + door_width/2 - 10, house_y + door_height/2)
    glEnd()
    
    # Windows (each drawn as two triangles)
    window_size = 30
    # Left window
    window_light = 9.0
    glColor3f(window_light, window_light + 0.1, 1.0)  
    glBegin(GL_TRIANGLES)
    # First triangle of left window
    glVertex2f(house_x - house_width/3 - window_size/2, house_y + house_height/2)
    glVertex2f(house_x - house_width/3 + window_size/2, house_y + house_height/2)
    glVertex2f(house_x - house_width/3 - window_size/2, house_y + house_height/2 + window_size)
    # Second triangle of left window
    glVertex2f(house_x - house_width/3 + window_size/2, house_y + house_height/2)
    glVertex2f(house_x - house_width/3 + window_size/2, house_y + house_height/2 + window_size)
    glVertex2f(house_x - house_width/3 - window_size/2, house_y + house_height/2 + window_size)
    glEnd()
    
    # Right window
    glBegin(GL_TRIANGLES)
    # First triangle of right window
    glVertex2f(house_x + house_width/3 - window_size/2, house_y + house_height/2)
    glVertex2f(house_x + house_width/3 + window_size/2, house_y + house_height/2)
    glVertex2f(house_x + house_width/3 - window_size/2, house_y + house_height/2 + window_size)
    # Second triangle of right window
    glVertex2f(house_x + house_width/3 + window_size/2, house_y + house_height/2)
    glVertex2f(house_x + house_width/3 + window_size/2, house_y + house_height/2 + window_size)
    glVertex2f(house_x + house_width/3 - window_size/2, house_y + house_height/2 + window_size)
    glEnd()
    
    # Window grills (+ sign) using GL_LINES
    glColor3f(0.2, 0.2, 0.3)  
    # Left window grill
    left_window_x = house_x - house_width/3
    left_window_y = house_y + house_height/2 + window_size/2
    
    # Horizontal line
    glBegin(GL_LINES)
    glVertex2f(left_window_x - window_size/2, left_window_y)
    glVertex2f(left_window_x + window_size/2, left_window_y)
    glEnd()
    
    # Vertical line
    glBegin(GL_LINES)
    glVertex2f(left_window_x, left_window_y - window_size/2)
    glVertex2f(left_window_x, left_window_y + window_size/2)
    glEnd()
    
    # Right window grill
    right_window_x = house_x + house_width/3
    right_window_y = house_y + house_height/2 + window_size/2
    
    # Horizontal line
    glBegin(GL_LINES)
    glVertex2f(right_window_x - window_size/2, right_window_y)
    glVertex2f(right_window_x + window_size/2, right_window_y)
    glEnd()
    
    # Vertical line
    glBegin(GL_LINES)
    glVertex2f(right_window_x, right_window_y - window_size/2)
    glVertex2f(right_window_x, right_window_y + window_size/2)
    glEnd()

# Draw Rain as Straight Vertical Lines 
def draw_rain():
    rain_visibility = 0.8 + 0.2 * day_night_factor
    glColor3f(rain_visibility , rain_visibility , 0.9)  
    
    for drop in rain_drops:
        x, y, speed = drop
        glBegin(GL_LINES)
        glVertex2f(x, y)
        glVertex2f(x + rain_direction, y - 20)  
        glEnd()

def update_rain():
    for drop in rain_drops:
        drop[1] -= drop[2]  

        # if rain goes below reset it 
        if drop[1] < -300:
            drop[0] = random.uniform(-400, 400)
            drop[1] = 300
            drop[2] = random.uniform(rain_speed * 0.8, rain_speed * 1.2)

# Update Day/Night 
def update_day_night():
    global background_color
    
    night_color = [0.1, 0.1, 0.3]  
    day_color = [0.6, 0.8, 1.0]   
    
    background_color[0] = night_color[0] + (day_color[0] - night_color[0]) * day_night_factor
    background_color[1] = night_color[1] + (day_color[1] - night_color[1]) * day_night_factor
    background_color[2] = night_color[2] + (day_color[2] - night_color[2]) * day_night_factor

#  Keyboard Controls 
def keyboard_listener(key, x, y):
    global rain_direction, day_night_factor
    
    # Key 1 (day)
    if key == b'1':
        day_night_factor = min(1.0, day_night_factor + 0.1)
        print(f"Changing to day: {day_night_factor:.2f}")
    
    # Key 2 (night)
    elif key == b'2':
        day_night_factor = max(0.0, day_night_factor - 0.1)
        print(f"Changing to night: {day_night_factor:.2f}")
    
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global rain_direction
    
    # Left arrow - Bend rain to the left
    if key == GLUT_KEY_LEFT:
        rain_direction = max(-5.0, rain_direction - 0.5)  # Increased step size
        print(f"Rain bending left: {rain_direction:.2f}")
    
    # Right arrow - Bend rain to the right
    elif key == GLUT_KEY_RIGHT:
        rain_direction = min(5.0, rain_direction + 0.5)  # Increased step size
        print(f"Rain bending right: {rain_direction:.2f}")
    
    glutPostRedisplay()


def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -300, 300, 0, 1)
    glMatrixMode(GL_MODELVIEW)

#  Display Func
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Set background color based on day/night cycle
    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    setup_projection()
    
    # (Ground)
    glColor3f(0.3, 0.6, 0.2)  # Green ground
    glBegin(GL_TRIANGLES)
    glVertex2f(-400, -300)
    glVertex2f(400, -300)
    glVertex2f(-400, -180)
    
    glVertex2f(400, -300)
    glVertex2f(400, -180)
    glVertex2f(-400, -180)
    glEnd()
    
    # Draw connected bushes behind the house
    draw_connected_bushes()
    
    # Draw the house
    draw_house()
    
    # Draw rain (in front of everything)
    draw_rain()
    
    glutSwapBuffers()

# Animation Func 
def animate():
    update_rain()
    update_day_night()
    glutPostRedisplay() # redraw or refresh

# Main Func
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(600, 000)
    glutCreateWindow(b"Task 1: Building a House in Rainfall")
    
    init_rain()
    
    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    
    
    glutMainLoop()

if __name__ == "__main__":
    main()






#task2###########################################



from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Global Variables 
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BOUNDARY_LEFT, BOUNDARY_RIGHT = -300, 300
BOUNDARY_BOTTOM, BOUNDARY_TOP = -250, 250

points = []
global_speed_factor = 1.0
frozen = False
blinking = False
last_blink_time = 0

#  Point Management Func
def create_point(x, y):
    color_r = random.uniform(0.1, 1.0)
    color_g = random.uniform(0.1, 1.0)
    color_b = random.uniform(0.1, 1.0)
    
    # Random direction
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    dx, dy = random.choice(directions)
    
    
    speed = random.uniform(0.1, 0.5)

    point = [x, y, color_r, color_g, color_b, dx, dy, speed, False, True, (color_r, color_g, color_b)]
    points.append(point)

# update points func
def update_points():
    global points
    
    for p in points:  
        if frozen:
            continue
            
        x, y, r, g, b, dx, dy, speed, blinking, visible, original_color = p  
        # Update position
        new_x = x + dx * speed * global_speed_factor
        new_y = y + dy * speed * global_speed_factor
        
        # Boundary collision detection and response
        if new_x <= BOUNDARY_LEFT or new_x >= BOUNDARY_RIGHT:
            p[5] = -dx  
            new_x = max(BOUNDARY_LEFT, min(new_x, BOUNDARY_RIGHT))
        if new_y <= BOUNDARY_BOTTOM or new_y >= BOUNDARY_TOP:
            p[6] = -dy 
            new_y = max(BOUNDARY_BOTTOM, min(new_y, BOUNDARY_TOP))
            
        # Update position
        p[0] = new_x  
        p[1] = new_y  

def handle_blinking():
    global last_blink_time, points
    
    current_time = time.time()
    if current_time - last_blink_time > 0.5:
        last_blink_time = current_time
        
        for p in points: 
            if p[8]:  
                p[9] = not p[9]  
# Draw boundary
def draw_boundary():
    glColor3f(1.0, 1.0, 1.0)  
    glLineWidth(2.0)
    
    glBegin(GL_LINES)
    # Bottom line
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_BOTTOM)
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_BOTTOM)
    # Top line
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_TOP)
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_TOP)
    # Right line
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_BOTTOM)
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_TOP)
    # Left line
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_BOTTOM)
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_TOP)
    glEnd()

def draw_points():
    
    for p in points:  
        x, y, r, g, b, dx, dy, speed, blinking, visible, original_color = p  
        
        if not visible:
            continue
            
        glColor3f(r, g, b)
        glPointSize(8)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

# Coordinate Conversion
def convert_coordinate(mouse_x, mouse_y): # mouse coordinate to opengl coordinate
    gl_x = BOUNDARY_LEFT + (mouse_x / WINDOW_WIDTH) * (BOUNDARY_RIGHT - BOUNDARY_LEFT)
    gl_y = BOUNDARY_BOTTOM + ((WINDOW_HEIGHT - mouse_y) / WINDOW_HEIGHT) * (BOUNDARY_TOP - BOUNDARY_BOTTOM)
    return gl_x, gl_y

# mouse lis
def mouse_listener(button, state, mouse_x, mouse_y):
    global points, blinking
    
    if frozen:
        return
        
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x, gl_y = convert_coordinate(mouse_x, mouse_y)
        
        if (BOUNDARY_LEFT <= gl_x <= BOUNDARY_RIGHT and 
            BOUNDARY_BOTTOM <= gl_y <= BOUNDARY_TOP):
            create_point(gl_x, gl_y)
            print(f"Created point at ({gl_x:.1f}, {gl_y:.1f})")
        else:
            print(f"Click outside boundary: ({gl_x:.1f}, {gl_y:.1f})")
    
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking = not blinking
        for p in points:  
            p[8] = blinking 
            if not blinking:
                p[9] = True  
                p[2], p[3], p[4] = p[10]  
        
        print(f"Blinking {'enabled' if blinking else 'disabled'}")

def keyboard_listener(key, x, y):
 
    global frozen
    
    if key == b' ':  
        frozen = not frozen
        print(f"Points {'frozen' if frozen else 'unfrozen'}")
    
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global global_speed_factor
    
    if frozen:
        return
        
    if key == GLUT_KEY_UP:
        global_speed_factor *= 1.5
        print(f"Speed increased to {global_speed_factor:.2f}")
    elif key == GLUT_KEY_DOWN:
        global_speed_factor /= 1.5
        global_speed_factor = max(0.1, global_speed_factor)  # Prevent negative speed
        print(f"Speed decreased to {global_speed_factor:.2f}")
    
    glutPostRedisplay()


def setup_projection():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(BOUNDARY_LEFT - 50, BOUNDARY_RIGHT + 50, 
               BOUNDARY_BOTTOM - 50, BOUNDARY_TOP + 50,0,1)
    glMatrixMode(GL_MODELVIEW)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    setup_projection()
    
    # Draw boundary
    draw_boundary()
    
    # draw points and update
    if not frozen:
        update_points()
        handle_blinking()
    
    draw_points()
    
    glutSwapBuffers()

def animate():
    glutPostRedisplay()
 
# Main Func
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Task 2: Building the Amazing Box")
    
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    
    # Register callback functions
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_listener)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    
    glutMainLoop()

if __name__ == "__main__":
    main()