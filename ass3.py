from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time


player_pos = [0, 0, 0]  
player_angle = 0  
player_life = 5
score = 0
bullets_missed = 0
game_over = False
cheat_mode = False
cheat_vision = False
first_person = False
move_speed = 8
rotate_speed = 5


camera_angle_x = 0
camera_angle_y = 45
camera_distance = 300
fovY = 120
GRID_LENGTH = 600

# Game Objects
bullets = []
enemies = []
enemy_scale = 1.0
scale_direction = 0.01
last_bullet_time = 0
last_enemy_move_time = 0
cheat_rotation_angle = 0
last_cheat_fire_time = 0


cheat_rotation_speed = 2.0  
cheat_fire_delay = 0.3  


for i in range(5):
    enemies.append({
        'pos': [random.randint(-400, 400), random.randint(-400, 400), 0],
        'active': True,
        'scale': 1.0,
        'move_speed': random.uniform(0.3, 0.8)
    })

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    window_width = glutGet(GLUT_WINDOW_WIDTH)
    window_height = glutGet(GLUT_WINDOW_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, window_width, 0, window_height)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    glColor3f(1, 0, 0)  
    
    glRasterPos2f(x, y)
    
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    
    if game_over:

        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 0, -30)
    
    
    glRotatef(player_angle, 0, 0, 1)
    
   # body
    glColor3f(0.65, 0.16, 0.16)  
    glPushMatrix()
    glTranslatef(0, 0, 30)  
    gluCylinder(gluNewQuadric(), 15, 15, 60, 20, 10)
    glPopMatrix()
    
    # head 
    glColor3f(0, 0, 0)  
    glPushMatrix()
    glTranslatef(0, 0, 90) 
    glutSolidSphere(12, 20, 20)
    glPopMatrix()
    
    # Right hand 
    glColor3f(1, 0, 0)  
    glPushMatrix()
    glTranslatef(10, 10, 70)  
    glRotatef(90, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 4, 3, 25, 10, 10)
    glPopMatrix()

    # Left hand 
    glPushMatrix()
    glTranslatef(10, -10, 70)  
    glRotatef(90, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 4, 3, 25, 10, 10)  
    glPopMatrix()

    #leg

    glColor3f(1, 0, 1)  
    glPushMatrix()
    glTranslatef(10, 10, 30) 
    glRotatef(0, 0, 1, 0) 
    gluCylinder(gluNewQuadric(), 8, 5, 25, 20, 10)  
    glPopMatrix()


    glColor3f(1, 0, 1)  
    glPushMatrix()
    glTranslatef(10, -10, 30) 
    glRotatef(0, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 8, 5, 25, 20, 10)  
    glPopMatrix()

    #  gun
    glColor3f(0.5, 0.5, 0.1)  
    glPushMatrix()
    glTranslatef(0, 0, 70)  
    glRotatef(90, 0, 1, 0)  
 
    gluCylinder(gluNewQuadric(), 3, 2, 40, 10, 10)
    
   
    glColor3f(0.4, 0.2, 0.1)  
    glTranslatef(0, 0, -10)
    gluCylinder(gluNewQuadric(), 3, 3, 15, 10, 10)
    
    glPopMatrix()
    
    glPopMatrix() 

def draw_enemy(enemy):
    if not enemy['active']:
        return
    
    glPushMatrix()
    glTranslatef(enemy['pos'][0], enemy['pos'][1], enemy['pos'][2])
    
    # Enemy body 
    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 20)  
    glScalef(enemy['scale'], enemy['scale'], enemy['scale'])
    glutSolidSphere(20, 20, 20)
    glPopMatrix()
    
    # Enemy head 
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 45)  
    glutSolidSphere(12, 20, 20)
    glPopMatrix()
    
    glPopMatrix()

def draw_bullet(bullet):
    glPushMatrix()
    glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
    glColor3f(1, 1, 0)  
    glutSolidCube(8) 
    glPopMatrix()
    
def draw_grid():
    square_size = 50
    half_grid = GRID_LENGTH
    
    glBegin(GL_QUADS)
    for x in range(-half_grid, half_grid, square_size):
        for y in range(-half_grid, half_grid, square_size):
            if ((x // square_size) + (y // square_size)) % 2 == 0:
                glColor3f(0.4, 0.8, 0.8)  
            else:
                glColor3f(1, 1, 1) 
            
            glVertex3f(x, y, 0)
            glVertex3f(x + square_size, y, 0)
            glVertex3f(x + square_size, y + square_size, 0)
            glVertex3f(x, y + square_size, 0)
    glEnd()
    
   
    boundary_height = 50
    boundary_thickness = 10
    
    # boundary
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(0, half_grid - boundary_thickness/2, boundary_height/2)
    glScalef(half_grid*2, boundary_thickness, boundary_height)
    glutSolidCube(1)
    glPopMatrix()
    
    # b
    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(0, -half_grid + boundary_thickness/2, boundary_height/2)
    glScalef(half_grid*2, boundary_thickness, boundary_height)
    glutSolidCube(1)
    glPopMatrix()
    
    # b
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(-half_grid + boundary_thickness/2, 0, boundary_height/2)
    glScalef(boundary_thickness, half_grid*2, boundary_height)
    glutSolidCube(1)
    glPopMatrix()
    
    # b
    glPushMatrix()
    glColor3f(1, 1, 0)
    glTranslatef(half_grid - boundary_thickness/2, 0, boundary_height/2)
    glScalef(boundary_thickness, half_grid*2, boundary_height)
    glutSolidCube(1)
    glPopMatrix()

def fire_bullet():
    global last_bullet_time
    
    current_time = time.time()
    if current_time - last_bullet_time < 0.2:  
        return
    
    last_bullet_time = current_time
    
    angle_rad = math.radians(player_angle)
    bullet_speed = 25
    

    bullet_start_x = player_pos[0] + 50 * math.cos(angle_rad)
    bullet_start_y = player_pos[1] + 50 * math.sin(angle_rad)
    bullet_start_z = player_pos[2] + 45  # Gun height at chest
    
    bullet = {
        'pos': [bullet_start_x, bullet_start_y, bullet_start_z],
        'vel': [bullet_speed * math.cos(angle_rad), 
                bullet_speed * math.sin(angle_rad), 
                0],
        'active': True
    }
    
    bullets.append(bullet)

def update_bullets():
    global bullets_missed, score
    
    for bullet in bullets[:]:
        if not bullet['active']:
            continue
            
       
        bullet['pos'][0] += bullet['vel'][0]
        bullet['pos'][1] += bullet['vel'][1]
        
        if (abs(bullet['pos'][0]) > GRID_LENGTH + 100 or 
            abs(bullet['pos'][1]) > GRID_LENGTH + 100):
            bullet['active'] = False
            if not cheat_mode:
                bullets_missed += 1
                if bullets_missed >= 10:
                    end_game()
            continue
        
        for enemy in enemies:
            if enemy['active']:
                dx = bullet['pos'][0] - enemy['pos'][0]
                dy = bullet['pos'][1] - enemy['pos'][1]
                dz = bullet['pos'][2] - (enemy['pos'][2] + 20)
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if distance < 30:  
                    bullet['active'] = False
                    score += 10
                    
            
                    enemy['pos'] = [random.randint(-400, 400), 
                                   random.randint(-400, 400), 0]
                    enemy['active'] = True
                    enemy['scale'] = 1.0
                    enemy['move_speed'] = random.uniform(0.3, 0.8)
                    break
    
  
    bullets[:] = [b for b in bullets if b['active']]

def update_enemies():
    global enemy_scale, scale_direction, player_life, last_enemy_move_time
    
    current_time = time.time()
    
    if current_time - last_enemy_move_time < 0.05:
        return
    
    last_enemy_move_time = current_time
    
    enemy_scale += scale_direction * 0.5
    if enemy_scale > 1.2 or enemy_scale < 0.8:
        scale_direction *= -1
    
    for enemy in enemies:
        if enemy['active']:
            enemy['scale'] = enemy_scale
            
          
            dx = player_pos[0] - enemy['pos'][0]
            dy = player_pos[1] - enemy['pos'][1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 50:
                move_speed = enemy['move_speed']
                enemy['pos'][0] += (dx / distance) * move_speed
                enemy['pos'][1] += (dy / distance) * move_speed
            
         
            enemy['pos'][0] = max(-GRID_LENGTH + 40, min(GRID_LENGTH - 40, enemy['pos'][0]))
            enemy['pos'][1] = max(-GRID_LENGTH + 40, min(GRID_LENGTH - 40, enemy['pos'][1]))
            
         
            player_dx = enemy['pos'][0] - player_pos[0]
            player_dy = enemy['pos'][1] - player_pos[1]
            player_distance = math.sqrt(player_dx*player_dx + player_dy*player_dy)
            
            if player_distance < 50:
                player_life -= 1
                if player_life <= 0:
                    end_game()
                enemy['pos'][0] += random.randint(-80, 80)
                enemy['pos'][1] += random.randint(-80, 80)

def find_closest_enemy_in_sight():
    closest_enemy = None
    closest_distance = float('inf')
    
    for enemy in enemies:
        if enemy['active']:
            dx = enemy['pos'][0] - player_pos[0]
            dy = enemy['pos'][1] - player_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            angle_to_enemy = math.degrees(math.atan2(dy, dx))
            if angle_to_enemy < 0:
                angle_to_enemy += 360
            
            current_angle = player_angle % 360
            
            angle_diff = min(
                abs(current_angle - angle_to_enemy),
                360 - abs(current_angle - angle_to_enemy)
            )
            
            if angle_diff <= 30 and distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
    
    return closest_enemy

def update_cheat_mode():
    global player_angle, last_cheat_fire_time
    
    if cheat_mode and not game_over:
        player_angle += cheat_rotation_speed
        player_angle %= 360  
        
        target_enemy = find_closest_enemy_in_sight()
        
        current_time = time.time()
        if target_enemy and current_time - last_cheat_fire_time > cheat_fire_delay:
            dx = target_enemy['pos'][0] - player_pos[0]
            dy = target_enemy['pos'][1] - player_pos[1]
            target_angle = math.degrees(math.atan2(dy, dx))
            
            old_angle = player_angle
            player_angle = target_angle
            
            fire_bullet()
            player_angle = old_angle
            last_cheat_fire_time = current_time

def end_game():
    global game_over
    if not game_over:  
        game_over = True

def reset_game():
    global player_pos, player_angle, player_life, score, bullets_missed
    global game_over, cheat_mode, cheat_vision, first_person
    global bullets, enemies, enemy_scale, scale_direction, cheat_rotation_angle
    
    player_pos = [0, 0, 0]
    player_angle = 0
    player_life = 5
    score = 0
    bullets_missed = 0
    game_over = False
    cheat_mode = False
    cheat_vision = False
    first_person = False
    
    bullets = []
    enemies = []
    enemy_scale = 1.0
    scale_direction = 0.01
    cheat_rotation_angle = 0
    
    for i in range(5):
        while True:
            x = random.randint(-400, 400)
            y = random.randint(-400, 400)
            if math.sqrt(x*x + y*y) > 150:
                enemies.append({
                    'pos': [x, y, 0],
                    'active': True,
                    'scale': 1.0,
                    'move_speed': random.uniform(0.3, 0.8)
                })
                break

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, cheat_vision, first_person
    
    if key == b'r' or key == b'R':
        reset_game()
        return
    
    if game_over:
        return
    
    if key == b'w' or key == b'W':
        angle_rad = math.radians(player_angle)
        player_pos[0] += move_speed * math.cos(angle_rad)
        player_pos[1] += move_speed * math.sin(angle_rad)
        
    elif key == b's' or key == b'S':
        angle_rad = math.radians(player_angle)
        player_pos[0] -= move_speed * math.cos(angle_rad)
        player_pos[1] -= move_speed * math.sin(angle_rad)
        
    elif key == b'a' or key == b'A':
        if not cheat_mode:
            player_angle += rotate_speed
            
    elif key == b'd' or key == b'D':
        if not cheat_mode:
            player_angle -= rotate_speed
            
    
    elif key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        if cheat_mode:
            print("CHEAT MODE: ON")
        else:
            print("CHEAT MODE: OFF")
            
            
    elif key == b'v' or key == b'V':
        if cheat_mode:
            first_person = not first_person
            if first_person:
                print("First-Person View: ON ")
            else:
                print("Third-Person View: ON")
        else:
            print("not working")
    
    # player to keep in boundaries
    player_pos[0] = max(-GRID_LENGTH + 40, min(GRID_LENGTH - 40, player_pos[0]))
    player_pos[1] = max(-GRID_LENGTH + 40, min(GRID_LENGTH - 40, player_pos[1]))

def specialKeyListener(key, x, y):
    global camera_angle_x, camera_angle_y, camera_distance
    
    if key == GLUT_KEY_UP:
        camera_angle_y += 2
        if camera_angle_y > 89:
            camera_angle_y = 89
            
    elif key == GLUT_KEY_DOWN:
        camera_angle_y -= 2
        if camera_angle_y < 1:
            camera_angle_y = 1
            
    elif key == GLUT_KEY_LEFT:
        camera_angle_x += 2
        
    elif key == GLUT_KEY_RIGHT:
        camera_angle_x -= 2

def mouseListener(button, state, x, y):
    global first_person
    
    if state == GLUT_DOWN:
        if button == GLUT_LEFT_BUTTON:
            if not game_over and not cheat_mode:  
                fire_bullet()
                
        elif button == GLUT_RIGHT_BUTTON:
            if not cheat_mode:
                first_person = not first_person
                if first_person:
                    print("First-Person View: ON")
                else:
                    print("Third-Person View: ON")
            else:
                print("Use V key to toggle view.")

def setupCamera():
    window_width = glutGet(GLUT_WINDOW_WIDTH)
    window_height = glutGet(GLUT_WINDOW_HEIGHT)
    
    aspect_ratio = window_width / window_height if window_height > 0 else 1.25
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, aspect_ratio, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if first_person:
        angle_rad = math.radians(player_angle)
        
        eye_x = player_pos[0]
        eye_y = player_pos[1]
        eye_z = player_pos[2] + 85 
     
        look_distance = 100
        center_x = eye_x + look_distance * math.cos(angle_rad)
        center_y = eye_y + look_distance * math.sin(angle_rad)
        center_z = eye_z 
        
        gluLookAt(eye_x, eye_y, eye_z,
                  center_x, center_y, center_z,
                  0, 0, 1)
    else:
        angle_rad_x = math.radians(camera_angle_x)
        angle_rad_y = math.radians(camera_angle_y)
        
        eye_x = player_pos[0] + camera_distance * math.cos(angle_rad_y) * math.sin(angle_rad_x)
        eye_y = player_pos[1] + camera_distance * math.cos(angle_rad_y) * math.cos(angle_rad_x)
        eye_z = player_pos[2] + camera_distance * math.sin(angle_rad_y) + 50
        
        gluLookAt(eye_x, eye_y, eye_z,
                  player_pos[0], player_pos[1], player_pos[2] + 30,
                  0, 0, 1)

def idle():
    if not game_over:
        update_bullets()
        update_enemies()
        update_cheat_mode()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    window_width = glutGet(GLUT_WINDOW_WIDTH)
    window_height = glutGet(GLUT_WINDOW_HEIGHT)
    
    glViewport(0, 0, window_width, window_height)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    light_position = [0.0, 0.0, 1.0, 0.0]  
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.8, 0.8, 0.8, 1.0])  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])  
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  
    
    
    setupCamera()
    
   
    glEnable(GL_DEPTH_TEST)
    
  
    draw_grid()
    
    # drw player
    if not first_person:
        draw_player()
    
    # Draw enemie
    for enemy in enemies:
        draw_enemy(enemy)
    
    # Draw bullets
    for bullet in bullets:
        draw_bullet(bullet)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, window_width, 0, window_height)  
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    center_x = window_width / 2  
    # player life
    life_text = f"Player's Life Remaining: {player_life}"
    text_width = len(life_text) * 9  
    draw_text(center_x - text_width/2, window_height - 30, life_text, GLUT_BITMAP_HELVETICA_18)
    
    # Game Score 
    score_text = f"Game Score: {score}"
    text_width = len(score_text) * 9
    draw_text(center_x - text_width/2, window_height - 60, score_text, GLUT_BITMAP_HELVETICA_18)
    
    # Bullet Missed 
    bullets_text = f"Bullet Missed: {bullets_missed}/10"
    text_width = len(bullets_text) * 9
    draw_text(center_x - text_width/2, window_height - 90, bullets_text, GLUT_BITMAP_HELVETICA_18)
    
    # cheat text
    if cheat_mode:
        glColor3f(0, 1, 0) 
        draw_text(20, window_height - 20, "CHEAT MODE: ACTIVE", GLUT_BITMAP_HELVETICA_12)
        if first_person:
            draw_text(20, window_height - 40, "VIEW: FIRST-PERSON", GLUT_BITMAP_HELVETICA_12)
        else:
            draw_text(20, window_height - 40, "VIEW: THIRD-PERSON", GLUT_BITMAP_HELVETICA_12)
    
    if game_over:
        glColor3f(1, 0, 0)  
        game_over_text = "GAME OVER"
        text_width = len(game_over_text) * 24  
        draw_text(center_x - text_width/4, window_height/2, game_over_text, GLUT_BITMAP_TIMES_ROMAN_24)
        
        glColor3f(1, 1, 0) 
        final_score_text = f"Final Score: {score}"
        text_width = len(final_score_text) * 9
        draw_text(center_x - text_width/2, window_height/2 - 50, final_score_text, GLUT_BITMAP_HELVETICA_18)
        
        restart_text = "Press R to restart"
        text_width = len(restart_text) * 9
        draw_text(center_x - text_width/2, window_height/2 - 80, restart_text, GLUT_BITMAP_HELVETICA_18)
    
   
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    
    screen_width = glutGet(GLUT_SCREEN_WIDTH)
    screen_height = glutGet(GLUT_SCREEN_HEIGHT)
    
    glutInitWindowSize(screen_width, screen_height)
    glutInitWindowPosition(0, 0)
    
    wind = glutCreateWindow(b"Bullet Frenzy - 3D Game with Cheat Mode")
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)
    

    glutMainLoop()

if __name__ == "__main__":
    main()