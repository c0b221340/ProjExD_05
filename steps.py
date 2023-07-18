import math
import random
import sys
import time
import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ

lr = (+1, -1)  # 右向きか左向きかを表す定数


class Player(pg.sprite.Sprite):
    """
    プレイヤーに関するクラス
    """
    def __init__(self, pos: tuple) -> None:
        """
        プレイヤー画像Surfaceを作成し、rectを設定する
        引数：プレイヤーの位置
        """
        super().__init__()
        self.image = pg.image.load("ex05/fig/3.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.muki = [pg.transform.flip(self.image, True, False), self.image]
        self.count = 0

    def update(self, screen: pg.Surface, count: int) -> None:
        """
        プレイヤーの向きの更新
        引数１: ゲームウィンドウのSurface
        引数２: コントロールの押された回数
        """
        screen.blit(self.muki[count%2], self.rect.center) 
        
    def move(self, dx: int, dy: int) -> None:
        """
        プレイヤーを移動させる
        引数：移動量
        """
        self.rect.move_ip(dx, dy)
        
    def change_img(self, screen: pg.Surface) -> None:
        """
        プレイヤーの画像を変更する
        """
        self.image = pg.image.load(f"ex05/fig/8.png")
        screen.blit(self.image, self.rect)


class Score_my():

    """
    スコアに関するクラス
    """
    def __init__(self) -> None:
        """
        スコアを0に初期化する
        """
        self.font = pg.font.SysFont("hgp創英角ポップ体", 50)
        self.color = (0, 0, 255)
        self.score = 0
        self.img = self.font.render(f"SCORE:{self.score}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT-50)
       
    def score_up(self, add: int) -> None:
        """
        スコアを増やす
        引数：増やす量
        """
        self.score = self.score + add

    def update(self, screen: pg.Surface) -> None:
        """
        スコアを更新する
        引数：ゲームウィンドウのSurface
        """
        self.img = self.font.render(f"SCORE:{self.score}", 0, self.color)
        screen.blit(self.img, self.rct)

        
class Limit:
    """
    制限時間に関するクラス
    """
    def __init__(self, limit: int) -> None:
        """
        制限時間を初期化する
        引数：制限時間
        """
        self.limit = limit
        self.font = pg.font.SysFont("hgp創英角ポップ体", 50)
        self.color = (255, 0, 0)
        self.img = self.font.render(f"LIMIT:{self.limit}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT-100)

    def update(self, screen: pg.Surface) -> None:
        """
        制限時間を更新する
        0以下になった場合制限時間が0で止まる
        引数：ゲームウィンドウのSurface
        """
        self.img = self.font.render(f"LIMIT:{math.floor(self.limit)}", 0, self.color)
        screen.blit(self.img, self.rct)
        if self.limit<=0:
            self.limit=0
        else:
            self.limit -= 1/50  # 1/50ずつ減らす


class Step(pg.sprite.Sprite):
    """
    階段に関するクラス
    """
    def __init__(self, pos: tuple) -> None:
        """
        階段画像Surfaceを作成し、rectを設定する
        引数：階段の位置
        """
        super().__init__()
        self.size = (150, 30)  # 階段のサイズ
        self.image = pg.Surface(self.size)
        pg.draw.rect(self.image, (255, 0, 0), [0, 0, *self.size])  # 赤い四角形を描画
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 位置を設定

    def update(self, screen: pg.Surface) -> None:
        """
        階段を移動させる
        引数：ゲームウィンドウのSurface
        """
        screen.blit(self.image, self.rect.center)


def main():
    pg.display.set_caption("こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex05/fig/pg_bg.jpg")  # 地上の絵
    bg_img2 = pg.image.load("ex05/fig/Untitled2_20230711183506.png")  # 空の絵
    player = Player((840,465))  # プレイヤーを作成
    steps = pg.sprite.Group()  # 階段をまとめるグループ
    count = 0  # 左右どちらを向いているかを表すカウント
    tmr = 0  # タイマー
    jump = False  # ジャンプフラグ
    clock = pg.time.Clock()
    limit=Limit(60)
    score = Score_my()
    first_flag = True
    sx = 800  # 階段のx座標
    first_screen = True  # 最初の背景を作成するためのフラグ
    by = 0  # 背景のy座標

    while True:
        #最初だけ地上の絵を表示して後は空のみを表示
        if first_screen == True:  # 最初の背景を生成する
            screen.blit(bg_img, [0,by])  # 地上の背景を描画
            if by >= 900:
                first_screen = False  # 2回目以降は作成しない
        else:
            screen.blit(bg_img2,[0,by])  # 空の背景を描画
        screen.blit(bg_img2,[0,by-900])
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:  # スペースキーが押されたら
                jump = True  # ジャンプフラグをTrueにする
                player.update(screen, count)  # プレイヤーを描画
                rand = random.choice(lr)  # 左右どちらに作成するかをランダムに決める
                sx += 200 * rand  # 200ずつ移動する
                if sx < 0 or sx+150 > WIDTH:  # 画面外に作成しないようにする
                    sx -= 400 * rand  # 逆方向に表示する
                steps.add(Step((sx, 0)))  # 階段を作成
                for step in steps:
                    step.rect.move_ip(0, 100)  # 100ずつ下に移動する
                    if step.rect.top > HEIGHT:  # 画面外に出たら削除する
                        step.kill()
                by += 100  # 背景を100ずつ下に移動する
                score.score_up(1)  # スコアを1増やす
                player.move(200 * lr[count%2], 0)  # 向いている方向に200移動する
            if event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:  # 左コントロールキーが押されたら
                count += 1  # 向きを変更するためにカウントを増やす
                player.update(screen, count)  # プレイヤーを描画

        if first_flag:  # 最初の階段を作成
            first_flag = False  # 2回目以降は作成しない
            for sy in range(400, 0, -100):  # 400, 300, 200, 100の4個を作成
                rand = random.choice(lr)    # 左右どちらに作成するかをランダムに決める
                sx += 200 * rand
                if sx < 0 or sx+150 > WIDTH:  # 画面外に作成しないようにする
                    sx -= 400 * rand
                steps.add(Step((sx, sy)))  # 階段を作成

        #座標が絵の一番上までいったときxの値を変えることで絵の無限生成をする(座標リセット)
        if by == 1000:
            by = 100

        if jump == True:  #初期状態を除く
            if len(pg.sprite.spritecollide(player,steps , False)) == 0 or limit.limit < 1:  #階段に乗っていないときか制限時間が0のとき
                if score.score >= 4:  # scoreが4以上のとき
                    screen.blit(bg_img2, [0, 0])  # 空の背景を描画
                else:
                    screen.blit(bg_img, [0, by])  # 地上の背景を描画
                steps.update(screen)  # 階段を描画
                score.update(screen)  # スコアを描画
                limit.update(screen)  # 制限時間を描画
                player.change_img(screen)  #失敗画像に変更
                #  GameOverと表示する
                font = pg.font.SysFont("hgp創英角ポップ体", 200)
                color = (0, 0, 255)  # 青色
                img = font.render("GameOver", 0, color)
                rct = img.get_rect()
                rct.center = (WIDTH/2, HEIGHT-700)  
                screen.blit(img, rct)
                pg.display.update()  
                time.sleep(2)  # 2秒間待つ
                return     
            limit.update(screen)
               
        player.update(screen, count)
        score.update(screen)
        steps.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()