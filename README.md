# ゲーム のタイトル
Step Up kokaton


## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
* こうかとんをキーボードで操作し、階段を上っていく縦スクロールゲーム
* クリアはなし、失敗しない限り続く
* 制限時間は一分

## ゲームの操作方法
* スペースキー押下で向いている方向に一段上る
* 左Ctrl押下で方向転換

# ゲームの実装
## 共通基本機能
* 主人公キャラクターに関するクラス
* 階段に関するクラス
* 初期の階段を三つ生成する
* 階段を三つまで登れる

## 担当追加機能
* スコア・タイマー機能  村重
* 方向転換機能          横川
* 無限スクロール機能    竜﨑 
* 階段のランダム生成機能　三宅
* ゲームの終了判定　町田

### 方向転換機能（担当：横川）
* 左Ctrl押下で向きを変更
* 同時にcountの数値を押下回数に応じて増やす
* countの押下回数を2で割った余りを用いて、あらかじめ作成したこうかとんの向きのリストから画像をもってくる

### スコア・タイマー機能（担当：村重）
* スコアとタイマーを左下に表示
* 一段上るごとにスコアを+1
* 制限時間が0になるとGameOver

### 無限スクロール機能（担当：竜崎）
* 背景が無限ループするように
* 主人公ではなく背景を動かすように変更
* 地面を離れると空の画像を繰り返すように

### 階段のランダム生成機能（担当：三宅）
* ランダムな位置に初期階段を表示
* スペースを押すごとに階段をランダム生成
* 階段が画面外に生成されないように

### ゲームの終了判定機能（担当：町田）
* 階段に乗れなかった際にゲームを終了する
* こうかとんの画像を変更する機能を追加
* 初期位置では判定されないように

### ToDo
- [ ]  変数名の統一
- [ ]  移動距離に応じて背景の変更をする

### メモ
* すべてのクラスに関係する関数は，クラスの外で定義してある
* １つ階段を上がるたびにscoreを＋＝１している。
* 主人公の向きと動きに関係するcountとlrはクラスの外で定義してある。
* 時間制限のクラスとスコアのクラスは別々