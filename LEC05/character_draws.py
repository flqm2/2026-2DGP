#pico2d 라이브러리 활성화
from pico2d import *

def draw_circle():
    print("draw_circle()")
    pass
def draw_square():
    print("draw_square()")
    pass
def draw_triangle():
    print("draw_triangle()")
    pass

while True:
    #캔버스 열기
    open_canvas(800, 600)
    update_canvas()

    character = load_image('character.png')
    character.draw(400, 300)

    draw_circle()
    draw_square()
    draw_triangle()
    pass

