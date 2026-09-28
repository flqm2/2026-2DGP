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
    RADIUS = 400
    while True:
        clear_canvas()
        x = (m.sin(RADIUS) * 200) + 400
        y = (m.cos(RADIUS) * 200) + 300
        character.draw(x, y)
        update_canvas()
        RADIUS += 0.01
        delay(0.01)
        if y <= 100.1:
            break
    pass
def draw_square():
    x, y = start_x, start_y
    clear_canvas()
    while True:
        if x >= 600 and y <= 400:
            y += 2
        elif y >= 400 and x >= 200:
            x -= 2
        elif x <= 200 and y >= 100:
            y -= 2
        else:
            x+=2
        clear_canvas()
        character.draw(x, y)
        update_canvas()
        delay(0.01)
        if x == start_x and y == start_y:
            break
    pass
def draw_triangle():
    print("draw_triangle()")
    pass

while True:
    draw_circle()
    draw_square()
    draw_triangle()
    pass

