#pico2d 라이브러리 활성화
from pico2d import *
import math as m

#캔버스 열기
open_canvas(800, 600)
character = load_image('character.png')

WIDTH, HIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HIGHT // 2
start_x, start_y = CENTER_X, CENTER_Y // 2



def draw_circle():
    clear_canvas()
    character.draw(400, 150)
    update_canvas()
    RADIUS = 150
    angle = 0
    while True:
        clear_canvas()
        x = (m.sin(angle) * RADIUS) + 400
        y = (-m.cos(angle) * RADIUS) + 300
        character.draw(x, y)
        update_canvas()
        angle += 0.01
        delay(0.01)
        if angle > 2 * m.pi:
            break
    pass
def draw_square():
    x, y = start_x, start_y
    clear_canvas()
    while True:
        if x >= 500 and y <= 400:
            y += 2
        elif y >= 400 and x >= 300:
            x -= 2
        elif x <= 300 and y >= start_y:
            y -= 2
        else:
            x+=2
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)
        if x == start_x and y <= start_y:
            break
    pass
def draw_triangle():
    x, y = start_x, start_y
    angle = m.radians(45)
    ismove = False
    ismove2 = False
    clear_canvas()
    while True:
        if ismove == False and ismove2 == False:
            x += m.sin(angle) * 2.5
            y += m.cos(angle) * 2.5
            if y >= 400:
                ismove = True
        elif x >= 200 and ismove:
            x -= 2
            if x <= 200:
                ismove2 = True
                ismove = False
        elif ismove2:
            x += m.sin(angle) * 2.5
            y -= m.cos(angle) * 2.5
            if x >= start_x and y <= start_y and ismove2:
                ismove2 = False
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)
        if x >= start_x and y <= start_y:
            break
    pass

while True:
    draw_circle()
    draw_square()
    draw_triangle()
    pass

