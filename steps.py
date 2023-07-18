import math
import random
import sys
import time

import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ


class Player(pg.sprite.Sprite):
    """
    プレイヤーに関するクラス
    """
    def __init__(self, pos):
        super().__init__()
        self.image = pg.image.load("ex05/fig/3.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.dir = 0
        self.jump = 0
        self.jump_power = 20
        self.jump_max = 2

    def update(self, screen: pg.Surface):
        screen.blit(self.image, self.rect.center)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)



class Step(pg.sprite.Sprite):
    """
    階段に関するクラス
    """
    def __init__(self, pos):
        super().__init__()
        # 200, 50 の赤い四角形を作成
        self.size = (150, 30)
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, (255, 0, 0), [0, 0, *self.size])
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, screen: pg.Surface):
        screen.blit(self.image, self.rect.center)


def main():
    pg.display.set_caption("こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #地上の絵
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
    #空の絵
    bg_img2 = pg.image.load("ex05/fig/Untitled2_20230711183506.png")
    player = Player((800,470))
    steps = pg.sprite.Group()
    tmr = 0
    clock = pg.time.Clock()
    first_flag = True
    #最初の背景を生成するための判断材料
    first_screen = True
    x = 0
    while True:
        #最初だけ地上の絵を表示して後は空のみを表示
        if first_screen == True:
            screen.blit(bg_img, [0,x])
            if x == 900:
                first_screen = False
        else:
            screen.blit(bg_img2,[0,x])
        screen.blit(bg_img2,[0,x-900])
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if first_flag:
                    first_flag = False
                    steps.add(Step((900,400)))
                    steps.add(Step((1100,300)))
                    steps.add(Step((1300,200)))
                    print(first_flag)
                else: 
                    #座標を100増やす
                    x+=100
                    player.update(screen)
                    steps.add(Step((1500,100)))
            #座標が絵の一番上までいったときxの値を変えることで絵の無限生成をする(座標リセット)
            if x == 1000:
                x = 100

        player.update(screen)
        steps.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()