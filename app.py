# 1. 导入必要模块
from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import uuid
import time
import threading
from flask_cors import CORS


# 2. 应用初始化配置
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 临时语音文件存储目录
AUDIO_FOLDER = "/tmp/temp_audio"

# 确保存储目录存在
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 初始化创建临时目录: {AUDIO_FOLDER}")


# 3. 定时清理功能实现
def clean_temp_files():
    """每10分钟清理一次临时语音文件"""
    while True:
        try:
            # 获取目录中的所有文件
            file_list = os.listdir(AUDIO_FOLDER)

            if not file_list:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 临时目录为空，无需清理")
                time.sleep(600)  # 等待10分钟
                continue

            # 统计删除的文件数量
            deleted_count = 0

            # 遍历并删除文件
            for filename in file_list:
                file_path = os.path.join(AUDIO_FOLDER, filename)

                # 只处理文件，不处理子目录
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 已删除: {filename}")
                    except PermissionError:
                        # 处理文件被占用的情况（如正在播放）
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 文件被占用，跳过: {filename}")
                    except Exception as e:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 删除 {filename} 失败: {str(e)}")

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 清理完成，共删除 {deleted_count} 个文件")

        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 清理线程错误: {str(e)}")

        finally:
            # 无论是否出现错误，都等待10分钟后再次执行
            time.sleep(600)


def start_cleanup_thread():
    """启动清理线程（确保只启动一次）"""
    try:
        # 检查是否已有清理线程在运行
        for thread in threading.enumerate():
            if thread.name == "TempFileCleaner":
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 清理线程已在运行")
                return

        # 创建并启动线程
        cleanup_thread = threading.Thread(
            target=clean_temp_files,
            name="TempFileCleaner",  # 给线程命名，便于识别
            daemon=True  # 守护线程，主程序退出时自动结束
        )
        cleanup_thread.start()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 清理线程已启动，每10分钟执行一次")

    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 启动清理线程失败: {str(e)}")


# 全局启动清理线程（关键修改：在WSGI模式下也会执行）
start_cleanup_thread()


# 卡片數據（全部使用繁體中文）
cards = [
    {
        "english": "America, Joe comes from America. Joe",
        "phonetic": "/əˈmerɪkə/",
        "chinese_word": "美國",
        "chinese_sentence": "Joe來自美國。說明某人來自美國的用法"
    },
    {
        "english": "American, Sandy has some American friends.",
        "phonetic": "/əˈmerɪkən/",
        "chinese_word": "美國人；美國的",
        "chinese_sentence": "Sandy有一些美國朋友。表示美國人的用法"
    },
    {
        "english": "ask, Ms. Chen likes to ask questions in her class.",
        "phonetic": "/æsk/",
        "chinese_word": "問",
        "chinese_sentence": "陳老師喜歡在她的班上問問題。表示詢問的動作"
    },
    {
        "english": "autumn (fall), Leaves change colors in autumn.",
        "phonetic": "/ˈɔːtəm/",
        "chinese_word": "秋天",
        "chinese_sentence": "葉子在秋天變色。描述秋天的自然現象"
    },
    {
        "english": "banana, Monkeys like bananas.",
        "phonetic": "/bəˈnɑːnə/",
        "chinese_word": "香蕉",
        "chinese_sentence": "猴子喜歡香蕉。表示香蕉這種水果"
    },
    {
        "english": "bank, The bank is next to my house.",
        "phonetic": "/bæŋk/",
        "chinese_word": "銀行",
        "chinese_sentence": "銀行在我家隔壁。說明銀行的位置"
    },
    {
        "english": "bat, Bats come out at night.",
        "phonetic": "/bæt/",
        "chinese_word": "蝙蝠",
        "chinese_sentence": "蝙蝠在晚上出沒。描述蝙蝠的生活習性"
    },
    {
        "english": "belt, This belt is too long.",
        "phonetic": "/belt/",
        "chinese_word": "皮帶",
        "chinese_sentence": "這條皮帶太長了。描述皮帶的長度"
    },
    {
        "english": "bench, We can take a rest on the bench.",
        "phonetic": "/bentʃ/",
        "chinese_word": "長椅",
        "chinese_sentence": "我們可以在長椅上休息一下。說明長椅的用途"
    },
    {
        "english": "bicycle (bike), Riding a bicycle is a good exercise.",
        "phonetic": "/ˈbaɪsɪkl/",
        "chinese_word": "腳踏車",
        "chinese_sentence": "騎腳踏車是很好的運動。說明騎腳踏車的好處"
    },
    {
        "english": "body, His whole body is in the water.",
        "phonetic": "/ˈbɒdi/",
        "chinese_word": "身體",
        "chinese_sentence": "他整個身體都在水裡。描述身體的狀態"
    },
    {
        "english": "bow, Bow to the teacher when she comes.",
        "phonetic": "/baʊ/",
        "chinese_word": "鞠躬",
        "chinese_sentence": "老師來時要向她鞠躬。表示尊敬的禮儀動作"
    },
    {
        "english": "bowl, I had a bowl of rice for lunch.",
        "phonetic": "/bəʊl/",
        "chinese_word": "碗",
        "chinese_sentence": "我午餐吃了一碗飯。表示碗的容量單位用法"
    },
    {
        "english": "brush, I brush my teeth twice a day.",
        "phonetic": "/brʌʃ/",
        "chinese_word": "刷",
        "chinese_sentence": "我一天刷兩次牙。表示清潔的動作"
    },
    {
        "english": "cage, There is a lion in the cage.",
        "phonetic": "/keɪdʒ/",
        "chinese_word": "籠子",
        "chinese_sentence": "籠子裡有一隻獅子。說明籠子的用途"
    },
    {
        "english": "candle, Blow out the candles!",
        "phonetic": "/ˈkændl/",
        "chinese_word": "蠟燭",
        "chinese_sentence": "吹蠟燭！生日等場合的常用語"
    },
    {
        "english": "chalk, The teacher is writing on the blackboard with a chalk.",
        "phonetic": "/tʃɔːk/",
        "chinese_word": "粉筆",
        "chinese_sentence": "老師正用粉筆寫黑板。說明粉筆的用途"
    },
    {
        "english": "child, The child is playing with his toys.",
        "phonetic": "/tʃaɪld/",
        "chinese_word": "小孩",
        "chinese_sentence": "那孩子正在玩他的玩具。描述小孩的活動"
    },
    {
        "english": "circle, Draw a circle on your paper.",
        "phonetic": "/ˈsɜːkl/",
        "chinese_word": "圓圈",
        "chinese_sentence": "在你的紙上畫一個圓。表示一種幾何形狀"
    },
    {
        "english": "clothes, We buy new clothes for the Chinese New Year.",
        "phonetic": "/kləʊðz/",
        "chinese_word": "衣服",
        "chinese_sentence": "我們過新年買新衣。說明衣服的購買習俗"
    },
    {
        "english": "cookie, My mom can bake cookies.",
        "phonetic": "/ˈkʊki/",
        "chinese_word": "餅乾",
        "chinese_sentence": "我的媽媽會烤餅乾。表示一種點心"
    },
    {
        "english": "cross, Be careful when you cross the road.",
        "phonetic": "/krɒs/",
        "chinese_word": "越過",
        "chinese_sentence": "穿越馬路時要小心。表示橫穿的動作"
    },
    {
        "english": "cry, The baby is crying.",
        "phonetic": "/kraɪ/",
        "chinese_word": "哭",
        "chinese_sentence": "那個寶寶在哭。描述哭泣的狀態"
    },
    {
        "english": "dance, Stacy dances very well.",
        "phonetic": "/dɑːns/",
        "chinese_word": "跳舞",
        "chinese_sentence": "Stacy舞跳得很好。描述跳舞的能力"
    },
    {
        "english": "dark, It’s dark in here.",
        "phonetic": "/dɑːk/",
        "chinese_word": "黑暗的",
        "chinese_sentence": "這裡面很黑。描述光線不足的狀態"
    },
    {
        "english": "die, My grandma died many years ago.",
        "phonetic": "/daɪ/",
        "chinese_word": "死",
        "chinese_sentence": "我奶奶多年前去世了。表示死亡的狀態"
    },
    {
        "english": "down, Sit down, please.",
        "phonetic": "/daʊn/",
        "chinese_word": "向下",
        "chinese_sentence": "請坐下。表示方向的副詞用法"
    },
    {
        "english": "drink, Drink more water in summer.",
        "phonetic": "/drɪŋk/",
        "chinese_word": "喝",
        "chinese_sentence": "夏天要喝更多水。表示飲用的動作"
    },
    {
        "english": "duck, The Yellow Duck is so cute.",
        "phonetic": "/dʌk/",
        "chinese_word": "鴨子",
        "chinese_sentence": "黃色小鴨真可愛。描述鴨子的可愛"
    },
    {
        "english": "elephant, Elephants have a long nose.",
        "phonetic": "/ˈelɪfənt/",
        "chinese_word": "大象",
        "chinese_sentence": "大象有長鼻子。描述大象的特徵"
    },
    {
        "english": "ever, Let me know if you ever see Frank.",
        "phonetic": "/ˈevə(r)/",
        "chinese_word": "曾經",
        "chinese_sentence": "如果你有看到Frank，跟我說一聲。表示曾經的副詞用法"
    },
    {
        "english": "fan, Lady Gaga has many fans.",
        "phonetic": "/fæn/",
        "chinese_word": "迷",
        "chinese_sentence": "Lady Gaga有很多歌迷。表示粉絲的意思"
    },
    {
        "english": "fly, Birds can fly.",
        "phonetic": "/flaɪ/",
        "chinese_word": "飛",
        "chinese_sentence": "鳥會飛。描述飛行的能力"
    },
    {
        "english": "free, Birds are free to fly.",
        "phonetic": "/friː/",
        "chinese_word": "自由的",
        "chinese_sentence": "鳥兒可以自由地飛。表示不受約束的狀態"
    },
    {
        "english": "French fries, They sell French fries at McDonald’s.",
        "phonetic": "/ˌfrentʃ ˈfraɪz/",
        "chinese_word": "薯條",
        "chinese_sentence": "麥當勞裡有賣薯條。表示一種食物"
    },
    {
        "english": "funny, Wesley is very funny.",
        "phonetic": "/ˈfʌni/",
        "chinese_word": "有趣的",
        "chinese_sentence": "Wesley很有趣。描述人的性格特點"
    },
    {
        "english": "gas, My car is running out of gas.",
        "phonetic": "/ɡæs/",
        "chinese_word": "汽油",
        "chinese_sentence": "我的車子快沒油了。表示汽車燃料"
    },
    {
        "english": "ghost, The little kid is afraid of ghosts.",
        "phonetic": "/ɡəʊst/",
        "chinese_word": "鬼",
        "chinese_sentence": "那個小孩很怕鬼。表示靈魂的概念"
    },
    {
        "english": "giant, Look at the giant pumpkin.",
        "phonetic": "/ˈdʒaɪənt/",
        "chinese_word": "巨大的",
        "chinese_sentence": "看那個巨大的南瓜。描述物體的大小"
    },
    {
        "english": "glasses, My grandpa has to put on glasses when he reads.",
        "phonetic": "/ˈɡlɑːsɪz/",
        "chinese_word": "眼鏡",
        "chinese_sentence": "我的爺爺閱讀時必須戴上眼鏡。說明眼鏡的用途"
    },
    {
        "english": "grade, She always get good grades.",
        "phonetic": "/ɡreɪd/",
        "chinese_word": "成績",
        "chinese_sentence": "她總是拿到好成績。表示學習成績"
    },
    {
        "english": "grow, These plants grow so fast.",
        "phonetic": "/ɡrəʊ/",
        "chinese_word": "生長",
        "chinese_sentence": "這些植物長得真快。描述生長的過程"
    },
    {
        "english": "guy, Look at the guy over there.",
        "phonetic": "/ɡaɪ/",
        "chinese_word": "人；傢伙",
        "chinese_sentence": "看著那邊那個人。表示對人的稱呼"
    },
    {
        "english": "Halloween, Kids like to dress up on Halloween.",
        "phonetic": "/ˌhæləʊˈiːn/",
        "chinese_word": "萬聖節",
        "chinese_sentence": "小孩子喜歡在萬聖節裝扮自己。描述節日習俗"
    },
    {
        "english": "hang, You can hang the picture on the wall.",
        "phonetic": "/hæŋ/",
        "chinese_word": "掛",
        "chinese_sentence": "你可以把那幅畫掛在牆上。表示懸掛的動作"
    },
    {
        "english": "hill, There is a hill across the river.",
        "phonetic": "/hɪl/",
        "chinese_word": "小山丘",
        "chinese_sentence": "過河後有個小山丘。描述地形特徵"
    },
    {
        "english": "hit, Don’t hit your brother.",
        "phonetic": "/hɪt/",
        "chinese_word": "打",
        "chinese_sentence": "別打你哥哥。表示攻擊的動作"
    },
    {
        "english": "hope, I hope it will go well.",
        "phonetic": "/həʊp/",
        "chinese_word": "希望",
        "chinese_sentence": "我希望它會進行得很順利。表示期望的心情"
    },
    {
        "english": "horse, Horses run very fast.",
        "phonetic": "/hɔːs/",
        "chinese_word": "馬",
        "chinese_sentence": "馬跑很快。描述馬的特點"
    },
    {
        "english": "hour, The program is two hours long.",
        "phonetic": "/ˈaʊə(r)/",
        "chinese_word": "小時",
        "chinese_sentence": "這個節目長兩小時。表示時間單位"
    },
    {
        "english": "ice, I put some ice in my coke.",
        "phonetic": "/aɪs/",
        "chinese_word": "冰",
        "chinese_sentence": "我在可樂裡加了一些冰塊。表示冰的用途"
    },
    {
        "english": "into, They ran into the hospital.",
        "phonetic": "/ˈɪntu/",
        "chinese_word": "到…裡",
        "chinese_sentence": "他們跑進醫院。表示進入的方向"
    },
    {
        "english": "join, Welcome to join us.",
        "phonetic": "/dʒɔɪn/",
        "chinese_word": "加入",
        "chinese_sentence": "歡迎加入我們。表示參與的動作"
    },
    {
        "english": "joy, His words bring me joy.",
        "phonetic": "/dʒɔɪ/",
        "chinese_word": "歡樂",
        "chinese_sentence": "他的話讓我開心。表示快樂的心情"
    },
    {
        "english": "juice, Would you like some juice?",
        "phonetic": "/dʒuːs/",
        "chinese_word": "果汁",
        "chinese_sentence": "你要來些果汁嗎？表示一種飲料"
    },
    {
        "english": "keep, You can keep these books.",
        "phonetic": "/kiːp/",
        "chinese_word": "保留；保持",
        "chinese_sentence": "你可以保有這些書。表示保留的意思"
    },
    {
        "english": "kick, Some children are kicking the soccer on the playground.",
        "phonetic": "/kɪk/",
        "chinese_word": "踢",
        "chinese_sentence": "一些小孩在操場上踢球。表示踢的動作"
    },
    {
        "english": "kind, What kind of movies do you like?",
        "phonetic": "/kaɪnd/",
        "chinese_word": "種類",
        "chinese_sentence": "你喜歡哪一種電影？表示類型的疑問"
    },
    {
        "english": "kiss, Dad kissed Mom.",
        "phonetic": "/kɪs/",
        "chinese_word": "親吻",
        "chinese_sentence": "爸爸親了媽媽。表示親密的動作"
    },
    {
        "english": "kitchen, She is preparing dinner in the kitchen.",
        "phonetic": "/ˈkɪtʃɪn/",
        "chinese_word": "廚房",
        "chinese_sentence": "她在廚房裡準備晚餐。表示廚房的用途"
    },
    {
        "english": "kite, We sometimes fly a kite on a sunny day.",
        "phonetic": "/kaɪt/",
        "chinese_word": "風箏",
        "chinese_sentence": "我們有時會在晴天放風箏。表示一種戶外活動"
    },
    {
        "english": "knee, Ben hurt his knee last week.",
        "phonetic": "/niː/",
        "chinese_word": "膝蓋",
        "chinese_sentence": "Ben上週傷了他的膝蓋。表示身體部位"
    },
    {
        "english": "lamp, Turn on the lamp when you read.",
        "phonetic": "/læmp/",
        "chinese_word": "檯燈",
        "chinese_sentence": "閱讀時把檯燈打開。說明檯燈的用途"
    },
    {
        "english": "later, See you later.",
        "phonetic": "/ˈleɪtə(r)/",
        "chinese_word": "待會",
        "chinese_sentence": "待會見。表示稍後的時間"
    },
    {
        "english": "leave, The train leaves at 4:30 p.m.",
        "phonetic": "/liːv/",
        "chinese_word": "離開",
        "chinese_sentence": "火車會在四點半駛離。表示出發的時間"
    },
    {
        "english": "lid, This lid is for the cup.",
        "phonetic": "/lɪd/",
        "chinese_word": "蓋子",
        "chinese_sentence": "這是那個杯子的蓋子。表示容器的蓋子"
    },
    {
        "english": "light, Could you turn on the light?",
        "phonetic": "/laɪt/",
        "chinese_word": "光",
        "chinese_sentence": "你可以把燈打開嗎？表示燈光"
    },
    {
        "english": "magic, Harry Potter has magic power.",
        "phonetic": "/ˈmædʒɪk/",
        "chinese_word": "魔力的",
        "chinese_sentence": "哈利波特擁有魔力。表示超自然的力量"
    },
    {
        "english": "mat, Put your cup on the mat.",
        "phonetic": "/mæt/",
        "chinese_word": "杯墊",
        "chinese_sentence": "把你的杯子放在杯墊上。表示杯墊的用途"
    },
    {
        "english": "meal, I eat three meals a day.",
        "phonetic": "/miːl/",
        "chinese_word": "一餐",
        "chinese_sentence": "我一天吃三餐。表示進食的次數"
    },
    {
        "english": "menu, Check the menu.",
        "phonetic": "/ˈmenjuː/",
        "chinese_word": "菜單",
        "chinese_sentence": "看一下菜單。表示餐廳的菜單"
    },
    {
        "english": "mile, The store is twenty miles from the station.",
        "phonetic": "/maɪl/",
        "chinese_word": "英哩",
        "chinese_sentence": "那間店離車站二十英哩。表示距離單位"
    },
    {
        "english": "move, My family might move to Kaohsiung next year.",
        "phonetic": "/muːv/",
        "chinese_word": "移動",
        "chinese_sentence": "我們家明年可能搬去高雄。表示搬家的動作"
    },
    {
        "english": "nature, Nature is beautiful.",
        "phonetic": "/ˈneɪtʃə(r)/",
        "chinese_word": "自然",
        "chinese_sentence": "自然就是美。描述自然的狀態"
    },
    {
        "english": "pipe, Some pipes are under the ground.",
        "phonetic": "/paɪp/",
        "chinese_word": "管子",
        "chinese_sentence": "一些管線在地底下。表示管道的存在"
    },
    {
        "english": "player, Bryant is a good basketball player.",
        "phonetic": "/ˈpleɪə(r)/",
        "chinese_word": "選手",
        "chinese_sentence": "Bryant是一位籃球好手。表示運動員"
    },
    {
        "english": "polite, You should be polite to your teacher.",
        "phonetic": "/pəˈlaɪt/",
        "chinese_word": "有禮貌的",
        "chinese_sentence": "對你的老師要有禮貌。表示行為舉止"
    },
    {
        "english": "poor, That poor man doesn’t have a house.",
        "phonetic": "/pɔː(r)/",
        "chinese_word": "貧窮的",
        "chinese_sentence": "那個窮人沒有家。描述經濟狀況"
    },
    {
        "english": "pound, Nina lost ten pounds.",
        "phonetic": "/paʊnd/",
        "chinese_word": "英磅",
        "chinese_sentence": "Nina減了十磅。表示體重單位"
    },
    {
        "english": "power, The boss has great power in his company.",
        "phonetic": "/ˈpaʊə(r)/",
        "chinese_word": "力量",
        "chinese_sentence": "這個老闆在公司裡有很大的權力。表示權力的概念"
    },
    {
        "english": "proud, We are so proud of you.",
        "phonetic": "/praʊd/",
        "chinese_word": "感到驕傲的",
        "chinese_sentence": "我們以你為榮。表示自豪的心情"
    },
    {
        "english": "rainbow, You can see a rainbow after the rain.",
        "phonetic": "/ˈreɪnbəʊ/",
        "chinese_word": "彩虹",
        "chinese_sentence": "你可以在雨後看到彩虹。描述自然現象"
    },
    {
        "english": "really, Did she really do this?",
        "phonetic": "/ˈriːəli/",
        "chinese_word": "真的",
        "chinese_sentence": "她真的這麼做嗎？表示疑問的強調"
    },
    {
        "english": "rest, Let’s take a rest and eat.",
        "phonetic": "/rest/",
        "chinese_word": "休息",
        "chinese_sentence": "我們休息一下吃點東西。表示休息的動作"
    },
    {
        "english": "rich, His business makes him rich.",
        "phonetic": "/rɪtʃ/",
        "chinese_word": "富有的",
        "chinese_sentence": "他的事業讓他賺了不少錢。描述經濟狀況"
    },
    {
        "english": "rise, My grandma always gets up before the sun rises.",
        "phonetic": "/raɪz/",
        "chinese_word": "升起",
        "chinese_sentence": "我的奶奶總是在日出前起床。表示太陽升起"
    },
    {
        "english": "rule, Our class made the rules together.",
        "phonetic": "/ruːl/",
        "chinese_word": "規則",
        "chinese_sentence": "我們班一起訂定這些規則。表示規定的制定"
    },
    {
        "english": "salt, You put too much salt in the noodles.",
        "phonetic": "/sɔːlt/",
        "chinese_word": "鹽",
        "chinese_sentence": "你在麵裡放太多鹽了。表示調味料"
    },
    {
        "english": "save, The prince saved the princess in the end.",
        "phonetic": "/seɪv/",
        "chinese_word": "拯救",
        "chinese_sentence": "王子在最後救了公主。表示救援的動作"
    },
    {
        "english": "set, You can set the machine here.",
        "phonetic": "/set/",
        "chinese_word": "放置",
        "chinese_sentence": "你可以把機器放這。表示安放的動作"
    },
    {
        "english": "sign, The sign says “No smoking.”",
        "phonetic": "/saɪn/",
        "chinese_word": "標示",
        "chinese_sentence": "標示寫著：禁止吸菸。表示告示牌的內容"
    },
    {
        "english": "simple, My grandma lives a simple life.",
        "phonetic": "/ˈsɪmpl/",
        "chinese_word": "簡單",
        "chinese_sentence": "我祖母的生活很簡單。描述生活狀態"
    },
    {
        "english": "sleep, Vivian goes to sleep at ten every night.",
        "phonetic": "/sliːp/",
        "chinese_word": "睡覺",
        "chinese_sentence": "Vivian每天晚上十點睡覺。表示睡眠的時間"
    },
    {
        "english": "spell, I can’t spell this word.",
        "phonetic": "/spel/",
        "chinese_word": "拼寫",
        "chinese_sentence": "我不會拼這個字。表示拼寫的能力"
    },
    {
        "english": "stairs, Don’t put things on the stairs.",
        "phonetic": "/steəz/",
        "chinese_word": "樓梯",
        "chinese_sentence": "不要在樓梯上放東西。表示樓梯的使用注意事項"
    },
    {
        "english": "together, Kate and I usually do homework together.",
        "phonetic": "/təˈɡeðə(r)/",
        "chinese_word": "一起",
        "chinese_sentence": "Kate和我常常一起做作業。表示共同進行的動作"
    },
    {
        "english": "touch, Don’t touch me.",
        "phonetic": "/tʌtʃ/",
        "chinese_word": "碰觸",
        "chinese_sentence": "別碰我。表示接觸的動作"
    },
    {
        "english": "trick, Trick or treat?",
        "phonetic": "/trɪk/",
        "chinese_word": "惡作劇",
        "chinese_sentence": "不給糖就搗蛋。萬聖節的常用語"
    },
    {
        "english": "truck, A truck stopped in front of me.",
        "phonetic": "/trʌk/",
        "chinese_word": "卡車",
        "chinese_sentence": "一台卡車停在我前面。表示一種交通工具"
    },
    {
        "english": "up, Stand up.",
        "phonetic": "/ʌp/",
        "chinese_word": "向上",
        "chinese_sentence": "站起來！表示方向的副詞用法"
    },
    {
        "english": "watermelon, We eat a lot of watermelon in summer.",
        "phonetic": "/ˈwɔːtəmelən/",
        "chinese_word": "西瓜",
        "chinese_sentence": "我們在夏天吃很多西瓜。表示一種水果"
    },
    {
        "english": "whale, The blue whale is the biggest animal in the world.",
        "phonetic": "/weɪl/",
        "chinese_word": "鯨魚",
        "chinese_sentence": "藍鯨是世界上最大的動物。描述鯨魚的特點"
    },
    {
        "english": "word, We learned five new words in the class.",
        "phonetic": "/wɜːd/",
        "chinese_word": "字",
        "chinese_sentence": "這堂課我們學了五個新單字。表示語言的基本單位"
    },
    {
        "english": "worker, All the workers are in this office.",
        "phonetic": "/ˈwɜːkə(r)/",
        "chinese_word": "工作人員",
        "chinese_sentence": "所有的員工都在這辦公室裡。表示從事工作的人"
    },
    {
        "english": "zebra, Are zebras white or black?",
        "phonetic": "/ˈzebrə/",
        "chinese_word": "斑馬",
        "chinese_sentence": "斑馬是白色或黑色呢？描述斑馬的顏色特徵"
    },
    {
        "english": "zero, Please enter “zero, nine, five.”",
        "phonetic": "/ˈzɪərəʊ/",
        "chinese_word": "零",
        "chinese_sentence": "請輸入「0-9-5」。表示數字0"
    }
]


# 5. 路由配置
@app.route('/')
def index():
    """首页路由，返回所有闪卡数据"""
    return render_template('index.html', cards=cards)


@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    """生成语音文件的接口"""
    # 获取前端发送的文本
    data = request.json
    text = data.get('text', '').strip()

    # 验证文本是否为空
    if not text:
        return "缺少文本參數", 400

    # 生成唯一的文件名
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    try:
        # 生成语音文件
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filepath)

        # 返回生成的语音文件
        return send_file(filepath, mimetype="audio/mp3", as_attachment=False)

    except Exception as e:
        return f"生成語音失敗: {str(e)}", 500


# 6. 本地调试入口（生产环境不执行）
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
