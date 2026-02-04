from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import math

# Global var
win_width, win_height = 500, 625
score = 0
game_over = False
paused = False
cheat_mode = False
last_time = 0
delta_time = 0

#Catcher var
catcher_x = win_width // 2
catcher_y = 5
catcher_width = 100
catcher_depth = 20
catcher_speed = 5

# Diamondvar
diamond_x = random.randint(50, win_width - 50)
diamond_y = win_height - 50
diamond_size = 7
diamond_speed = 150
diamond_color = (1.0, 1.0, 1.0)
diamond_acceleration = 25

# Button var
button_size = 30
restart_button = (40, win_height - 30)
play_pause_button = (win_width // 2, win_height - 30)
exit_button = (win_width - 30, win_height - 30)

# mpl
def zone_finder(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  # dx >= 0 and dy < 0
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:  # dx >= 0 and dy < 0
            return 6

def cnvt_to_zn0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def cnvt_from_zn0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_mpl(x1, y1, x2, y2):
    zone = zone_finder(x1, y1, x2, y2)
    x1_z0, y1_z0 = cnvt_to_zn0(x1, y1, zone)
    x2_z0, y2_z0 = cnvt_to_zn0(x2, y2, zone)

    if x1_z0 > x2_z0:
        x1_z0, y1_z0, x2_z0, y2_z0 = x2_z0, y2_z0, x1_z0, y1_z0
    
    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    
    x = x1_z0
    y = y1_z0
    
    while x <= x2_z0:
        x_orig, y_orig = cnvt_from_zn0(x, y, zone)
        draw_pixel(x_orig, y_orig)
        
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def bright_color():
    colors = [
        (1.0, 0.0, 0.0),    
        (0.0, 1.0, 0.0),   
        (0.0, 0.0, 1.0),    
        (0.5, 0.0, 1.0),    
        (1.0, 1.0, 1.0),  
        (1.0, 1.0, 0.0),  
        (1.0, 0.0, 1.0),    
        (0.0, 1.0, 1.0),    
        (1.0, 0.5, 0.0),      
        (0.0, 1.0, 0.5),    
        (1.0, 0.0, 0.5),    
        (0.5, 1.0, 0.0),    
    ]
    return random.choice(colors)


def draw_diamond(x, y, size, color):
    glColor3f(*color)
    draw_mpl(x, y - size-5, x + size, y)  
    draw_mpl(x + size, y, x, y + size+5)  
    draw_mpl(x, y + size+5, x - size, y)  
    draw_mpl(x - size, y, x, y - size-5)  


def draw_catcher(x, y, width, depth, color):
    glColor3f(*color)
    
    draw_mpl(x - width//2, y + depth, x + width//2, y + depth)
    bottom_width = (width+50) // 2
    draw_mpl(x - bottom_width//2, y, x + bottom_width//2, y)
    draw_mpl(x - width//2, y + depth, x - bottom_width//2, y)
    draw_mpl(x + width//2, y + depth, x + bottom_width//2, y)

def draw_restart_button(x, y, size):
    glColor3f(0.0, 0.8, 0.8) 
    draw_mpl(x + (size+20)//2, y, x - size//2, y) 
    draw_mpl(x - size//2, y, x - (size-50)/4, y - (size+30)//3) 
    draw_mpl(x - size//2, y, x - (size-50)//4, y + (size+30)//3) 

def draw_play_pause_button(x, y, size):
    if paused:
        glColor3f(1.0, 0.8, 0.0)  
        draw_mpl(x - size//3, y - size//2, x - size//3, y + size//2)
        draw_mpl(x - size//3, y + (size)//2, x + size//3, y)
        draw_mpl(x + size//3, y, x - size//3, y - (size)//2)
    else:
        glColor3f(1.0, 0.8, 0.0) 
        draw_mpl(x - size//3, y - size//2, x - size//3, y + (size+20)//2)
        draw_mpl(x + size//3, y - size//2, x + size//3, y + (size+20)//2)

def draw_exit_button(x, y, size):
    glColor3f(1.0, 0.0, 0.0) 
    draw_mpl(x - size//2, y - size//2, x + size//2, y + size//2)
    draw_mpl(x - size//2, y + size//2, x + size//2, y - size//2)


def collision():
    catcher_left = catcher_x - catcher_width // 2
    catcher_right = catcher_x + catcher_width // 2
    catcher_top = catcher_y + catcher_depth
    catcher_bottom = catcher_y
    
    diamond_left = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_top = diamond_y + diamond_size
    diamond_bottom = diamond_y - diamond_size
    
    return (diamond_right > catcher_left and 
            diamond_left < catcher_right and 
            diamond_bottom < catcher_top and 
            diamond_top > catcher_bottom)

def update_diamond():
    global diamond_y, diamond_speed, score, game_over, diamond_x, diamond_color
    
    if not paused and not game_over:
        diamond_y -= diamond_speed * delta_time
        
        diamond_speed += diamond_acceleration * delta_time
        
        if diamond_y < catcher_y + catcher_depth and collision():
            score += 1
            print(f"Score: {score}")  
            reset_diamond()
       
        elif diamond_y < 0:
            game_over = True
            print(f"Game Over! Final Score: {score}")

def reset_diamond():
    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(50, win_width - 50)
    diamond_y = win_height - 50
    diamond_color = bright_color()

def update_catcher():
    global catcher_x
    
    if cheat_mode and not paused and not game_over:
       
        time_to_catch = (diamond_y - (catcher_y + catcher_depth)) / diamond_speed
        
 
        distance_to_cover = diamond_x - catcher_x
        required_speed = distance_to_cover / time_to_catch if time_to_catch > 0 else 0
        
        
        cheat_speed = 200
        

        if abs(distance_to_cover) > 1:  
            move_direction = 1 if distance_to_cover > 0 else -1
            move_distance = cheat_speed * delta_time
            
            
            if abs(distance_to_cover) < move_distance:
                catcher_x = diamond_x  
            else:
                catcher_x += move_direction * move_distance
        
        
        catcher_x = max(catcher_width//2, min(win_width - catcher_width//2, catcher_x))

def restart_game():
    global score, game_over, paused, diamond_speed, catcher_x
    score = 0
    game_over = False
    paused = False
    diamond_speed = 150
    catcher_x = win_width // 2
    reset_diamond()
    print("Starting Over")


keys_pressed = {
    GLUT_KEY_LEFT: False,
    GLUT_KEY_RIGHT: False
}

def keyboard_listener(key, x, y):
    global cheat_mode
    
    if key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        print(f"Cheat mode: {'ON' if cheat_mode else 'OFF'}")
    
    glutPostRedisplay()

def specialK_press(key, x, y):
    if key in [GLUT_KEY_LEFT, GLUT_KEY_RIGHT]:
        keys_pressed[key] = True

def specialK_realease(key, x, y):
    if key in [GLUT_KEY_LEFT, GLUT_KEY_RIGHT]:
        keys_pressed[key] = False

def handle_movement():
    global catcher_x
    
    if not paused and not game_over and not cheat_mode:
        if keys_pressed[GLUT_KEY_LEFT]:
            catcher_x -= catcher_speed * delta_time
        if keys_pressed[GLUT_KEY_RIGHT]:
            catcher_x += catcher_speed * delta_time
        
        catcher_x = max(catcher_width//2, min(win_width - catcher_width//2, catcher_x))

def mouse_listener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
       
        gl_y = win_height - y
        
      
        if (abs(x - restart_button[0]) < button_size and 
            abs(gl_y - restart_button[1]) < button_size):
            restart_game()
        
    
        elif (abs(x - play_pause_button[0]) < button_size and 
              abs(gl_y - play_pause_button[1]) < button_size):
            global paused
            paused = not paused
            print("Game", "paused" if paused else "resumed")
        
        elif (abs(x - exit_button[0]) < button_size and 
              abs(gl_y - exit_button[1]) < button_size):
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()
    
    glutPostRedisplay()

def display():
    global last_time, delta_time
    
 
    current_time = time.time()
    if last_time == 0:
        delta_time = 0.016
    else:
        delta_time = current_time - last_time
    last_time = current_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, win_width, 0, win_height)
    glMatrixMode(GL_MODELVIEW)
    
    
    handle_movement()
    
    
    if not paused:
        update_diamond()
        update_catcher()
    
   
    if game_over:
        draw_catcher(catcher_x, catcher_y, catcher_width, catcher_depth, (1.0, 0.0, 0.0))
    else:
        draw_catcher(catcher_x, catcher_y, catcher_width, catcher_depth, (1.0, 1.0, 1.0))
    
    if not game_over:
        draw_diamond(diamond_x, diamond_y, diamond_size, diamond_color)
    

    draw_restart_button(*restart_button, button_size)
    draw_play_pause_button(*play_pause_button, button_size)
    draw_exit_button(*exit_button, button_size)
    
    glutSwapBuffers()

def idle_func():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(win_width, win_height)
    glutInitWindowPosition(650, 0)
    glutCreateWindow(b"Catch Diamond")
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(2.0)
    
    glutDisplayFunc(display)
    glutIdleFunc(idle_func)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(specialK_press)
    glutSpecialUpFunc(specialK_realease)
    glutMouseFunc(mouse_listener)
    
    reset_diamond()
    
    glutMainLoop()

if __name__ == "__main__":
    main()