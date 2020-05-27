from enum import Enum

#マスの種類
class Masstype(Enum):
    Blank = ('0' , '　')
    Box = ('1' , '人')
    Wall = ('2' , '壁')
    You = ('3' , '貞')
    Goal = ('4' , '穴')

    #マス情報取得
    def get_mass_type(ch):
        for mass_type in Masstype:
            if mass_type.value[0] == ch:
                return mass_type

#マップ情報の管理
class Massinfo():
    #ゴールの有無設定
    def __init__(self, mass_type):
        self.mass_type = mass_type
        if mass_type == Masstype.Goal:
            self.goal = True
        else:
            self.goal = False

    #表示文字を取得
    def get_disp(self):
        return self.mass_type.value[1]
#マップ出力
def disp_map(souko_map):
    for row in souko_map:
        row_str = ''
        for mass in row:
            row_str = row_str + mass.get_disp()
        print(row_str)

#マップ情報を生成
def create_map_info():
    #ファイルからマップ情報を取得
    f = None
    try:
        file_name = 'map.txt'
        print(file_name + 'からマップ情報取得')
        f = open(file_name)
        map_str = f.read()
    except Exception as e:
        print('マップ情報取得失敗')
        raise e
    #ファイルを開いていたら閉じる
    finally:
        if f is not None:
            f.close()

    #マップ情報を2次元配列で生成
    lines = map_str.split('\n')
    souko_map = []
    row = 0
    for line in lines:
        souko_map.append([])
        for ch in line:
            souko_map[row].append(Massinfo(Masstype.get_mass_type(ch)))
        row = row + 1

    #マップ情報を返却
    return souko_map

#諸々の現在値を求める関数
def search_map(mass_type,souko_map):
    result = []
    for y , row in enumerate(souko_map):
        for x , mass_info in enumerate(row):
            if mass_info.mass_type == mass_type:
                coordinate = (y, x)
                result.append(coordinate)
    return result


#キーの設定
class Keytype(Enum):
        #入力値、名前
        UP = ('w','上',)
        DOWN = ('z','下')
        LEFT = ('a','左')
        RIGHT = ('s','右')
        #入力値についての関数
        def check_key(input):
            if  input == 'w':
                return True
            elif input == 'z':
                return True
            elif input == 'a':
                return True
            elif input == 's':
                return True
            else:
                return False
        #入力された文字を照合
        def get_key(input):
            if Keytype.UP.value[0] == input:
                return Keytype.UP
            if Keytype.DOWN.value[0] == input:
                return Keytype.DOWN
            if Keytype.LEFT.value[0] == input:
                return Keytype.LEFT
            if Keytype.RIGHT.value[0] == input:
                return Keytype.RIGHT

#キャラを動かす
def kyara_move(input,souko_map):
    youser_key = Keytype.get_key(input)
    ynext = 0
    xnext = 0
    #キャラの動き
    if Keytype.UP == youser_key:
        ynext -= 1
    elif Keytype.DOWN == youser_key:
        ynext += 1
    if Keytype.LEFT == youser_key:
        xnext -= 1
    elif Keytype.RIGHT == youser_key:
        xnext += 1

    #キャラの現在値を取得
    search_you = search_map(Masstype.You,souko_map)
    search_you_y = search_you[0][0]
    search_you_x = search_you[0][1]

    #キャラの移動先の値を取得
    next_search_you_y = search_you_y + ynext
    next_search_you_x = search_you_x + xnext


    #一つ目の箱の現在値
    #box_1_y = search_box[0][0]
    #box_1_x = search_box[0][1]
    #二つ目の箱の現在値
    #box_2_y = search_box[1][0]
    #box_2_x = search_box[1][1]

    #箱の移動先の数値を取得
    #一つ目の箱の移動先の数値
    #next_box_1_y = box_1_y + ynext
    #next_box_1_x = box_1_x + xnext
    #二つ目の箱の移動先の数理
    #next_box_2_y = box_2_y + ynext
    #next_box_2_x = box_2_x + xnext

    #移動先が壁の場合
    if souko_map[next_search_you_y][next_search_you_x].mass_type == Masstype.Wall:
        print('　　抜けれないよ～')
        print(' ')
        return souko_map

    #移動可能な場合
    else:
        #移動先が箱の場合
        #箱の移動先の数理
        next_box_y = next_search_you_y + ynext
        next_box_x = next_search_you_x + xnext

        #箱の移動
        if souko_map[next_search_you_y][next_search_you_x].mass_type == Masstype.Box:
            #箱の先が壁の場合
            if souko_map[next_box_y][next_box_x].mass_type == Masstype.Wall:
                print('　　埋められないよ～')
                print(' ')
                return souko_map

                #箱の移動先が別の箱の場合
            elif souko_map[next_box_y][next_box_x].mass_type == Masstype.Box:
                print('　　合体できないよ～')
                print(' ')
                return souko_map

            #箱の先がゴールの場合
            elif  souko_map[next_box_y][next_box_x].goal == True:
                print('　　ボッシュートです！！')
                print(' ')
                souko_map[next_box_y][next_box_x].mass_type = Masstype.Goal

            #何もなければ箱を移動
            else:
                souko_map[next_box_y][next_box_x].mass_type = Masstype.Box

        #キャラ移動
        souko_map[next_search_you_y][next_search_you_x].mass_type = Masstype.You

        #キャラがゴールを通過したらゴールを再表示
        if souko_map[search_you_y][search_you_x].goal == True:
            souko_map[search_you_y][search_you_x].mass_type = Masstype.Goal

        else:
            #キャラの移動後のマスを空白にする
            souko_map[search_you_y][search_you_x].mass_type = Masstype.Blank

    return souko_map


#ゲーム処置
def game():
    #マップ情報読み込み
    souko_map = create_map_info()

    #諸々の処理
    while True:
        #マップ表示
        disp_map(souko_map)

        #入力処理
        print('w:上、z:下、s:右、a:左、con:コンティニュー')
        move_player = input('文字を入れてください:')
        #マップをリセットしたい場合
        if move_player == 'con':
            print('　　マップを初期化しました')
            print(' ')
            print(' ')
            souko_map = create_map_info()
            continue
        #移動用の文字以外を入れられた場合
        if not Keytype.check_key(move_player):
            print('　　呪うよ？')
            print(' ')
            print(' ')
            continue

        #移動関係
        souko_map = kyara_move(move_player,souko_map)

        #ゴール判定
        #箱の現在値の取得
        search_box = search_map(Masstype.Box,souko_map)
        #箱がゴールに入り、マップから消えて終了とする
        if not search_box:
            print('呪呪くる～きっとくる～呪呪')
            disp_map(souko_map)
            break

        print(' ')
game()
