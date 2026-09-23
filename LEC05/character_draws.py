#pico2d 라이브러리 활성화
from pico2d import *

#캔버스 열기
open_canvas(800, 600)
update_canvas()

character = load_image('character.png')
update_canvas()


delay(10)

while True:
    character.draw(400, 300)
    pass

close_canvas()

