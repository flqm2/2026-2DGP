#pico2d 라이브러리 활성화
from pico2d import *
import math as m

#캔버스 열기
open_canvas(800, 600)
character = load_image('character.png')

WIDTH, HIGHT = 800, 600
CENTER_X, CENTER_Y = WIDTH // 2, HIGHT // 2
start_x, start_y = CENTER_X, CENTER_Y // 2
x, y = start_x, start_y



def draw_circle():
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    pass
def draw_square():
    print("draw_square()")
    pass
def draw_triangle():
    print("draw_triangle()")
    pass

while True:
    draw_circle()
    draw_square()
    draw_triangle()
    pass

