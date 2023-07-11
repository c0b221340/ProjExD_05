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

    def change_img(self,screen: pg.Surface):  #失敗画像に変更する
        self.image = pg.transform.rotozoom(pg.image.load(f"ex05/fig/8.png"), 0, 2.0)
        screen.blit(self.image, self.rect)




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
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")

    player = Player((800,470))
    steps = pg.sprite.Group()

    tmr = 0
    score = 0
    clock = pg.time.Clock()

    first_flag = True

    while True:
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if first_flag:
                    first_flag = False
                    steps.add(Step((900,400)))
                    steps.add(Step((1100,300)))
                    # steps.add(Step((1300,200)))
                else:
                    score += 1
                    # player.update(screen)
                    # steps.add(Step((1500,100)))
                    player.move(150, -100)
        print(len(pg.sprite.spritecollide(player,steps , False, collided=pg.sprite.collide_rect)))
        
        if score != 0:  #初期状態を除く
            if len(pg.sprite.spritecollide(player,steps , False)) == 0:  #階段に乗っていないとき
                screen.blit(bg_img, [0, 0])  #背景を描画
                steps.update(screen)  #階段を描画
                player.change_img(screen)  #失敗画像に変更
                pg.display.update()  
                time.sleep(2)
                return
        #print(player.rect, 1)
        #print(*[s.rect for s in steps], 2)　　＃画像が重なっているかの確認
        screen.blit(bg_img, [0, 0])
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