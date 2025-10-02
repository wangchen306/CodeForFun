from 序列 import LiuQin, WuXing
import copy


class Yao:
    """表示爻的类"""
    def __init__(self, number):
        self.num = number
        self.states = {6: '老阴', 7: '少阳', 8: '少阴', 9: '老阳'}
        self.contents()

    def contents(self):
        """更新爻的信息"""
        self.yin_yang = (self.num+1) % 2 # 0为阳1为阴
        self.state = self.states[self.num]
        self.image = '--' if self.yin_yang else '——'

    def change(self):
        """爻变"""
        if self.num == 6: self.num = 7
        if self.num == 9: self.num = 8
        self.contents()

class Gua8:
    """八卦"""
    def __init__(self, number):
        names = ['乾', '兑', '离', '震', '巽', '坎', '艮', '坤']
        images = ['天', '泽', '火', '雷', '风', '水', '山', '地']
        self.name, self.image = names[number], images[number]

class Gua64:
    """六十四卦"""
    def __init__(self, yaos):
        """输入六个爻对象构成的列表"""
        self.yaos = yaos
        self.numbering()
        self.naming()
        self.bagong()
        self.imaging()
        self.deco_wuxing()
        self.deco_liuqin()
        self.write_content()

        if self.num[0] != self.num[1]:
            self.long_name = f'\t\t{self.image[0]}{self.image[1]}{self.name}\t'
        else:
            self.long_name = f'\t\t{self.name}为{self.image[0]}'

    def imaging(self):
        """卦象：[上卦卦象, 下卦卦象]"""
        self.image = [ Gua8(self.num[0]).image, Gua8(self.num[1]).image ]

    def naming(self):
        """生成卦名"""
        names = {
                0: ['乾', '履', '同人', '无妄', '姤', '讼', '遁', '否'],
                1: ['夬', '兑', '革', '随', '大过', '困', '咸', '萃'],
                2: ['大有', '睽', '离', '噬嗑', '鼎', '未济', '旅', '晋'],
                3: ['大壮', '归妹', '丰', '震', '恒', '解', '小过', '豫'],
                4: ['小畜', '中孚', '家人', '益', '巽', '涣', '渐', '观'],
                5: ['需', '节', '既济', '屯', '井', '坎', '蹇', '比'],
                6: ['大畜', '损', '贲', '颐', '蛊', '蒙', '艮', '剥'],
                7: ['泰', '临', '明夷', '复', '升', '师', '谦', '坤']
                } # 六十四卦名
        self.name = names[self.num[0]][self.num[1]]

    def numbering(self):
        """生成卦数[上卦数, 下卦数]"""
        self.num = [0, 0]
        s0, s1 = '', ''
        for yao in self.yaos[0: 3]:
            s1 += str(yao.yin_yang)
        self.num[1] = int(s1, 2)

        for yao in self.yaos[3: ]:
            s0 += str(yao.yin_yang)
        self.num[0] = int(s0, 2)

    def bagong(self):
        gongs = {
                0: ['乾', '姤', '遁', '否', '观', '剥', '晋', '大有', '金'],
                1: ['兑', '困', '萃', '咸', '蹇', '谦', '小过', '归妹', '金'],
                2: ['离', '旅', '鼎', '未济', '蒙', '涣', '讼', '同人', '火'],
                3: ['震', '豫', '解', '恒', '升', '井', '大过', '随', '木'],
                4: ['巽', '小畜', '家人', '益', '无妄', '噬嗑', '颐', '蛊', '木'],
                5: ['坎', '节', '屯', '既济', '革', '丰', '明夷', '师', '水'],
                6: ['艮', '贲', '大畜', '损', '睽', '履', '中孚', '渐', '土'],
                7: ['坤', '复', '临', '泰', '大壮', '夬', '需', '比', '土']
        } # 八宫
        shis = [6, 1, 2, 3, 4, 5, 4, 3]
        for v in gongs.values():
            for i in range(8):
                if self.name == v[i]:
                    self.gong, self.wu_xing = v[0], v[-1]
                    shi = shis[i]
                    self.shi_ying = [ shi-1, (shi+3)%6-1 ] # 存储世应（以0开始）
                    break
            else:
                continue
            break

    def deco_wuxing(self):
        """六爻的地支五行"""
        wxs = {
                0: ['子水', '寅木', '辰土', '午火', '申金', '戌土'],
                1: ['巳火', '卯木', '丑土', '亥水', '酉金', '未土'],
                2: ['卯木', '丑土', '亥水', '酉金', '未土', '巳火'],
                3: ['子水', '寅木', '辰土', '午火', '申金', '戌土'],
                4: ['丑土', '亥水', '酉金', '未土', '巳火', '卯木'],
                5: ['寅木', '辰土', '午火', '申金', '戌土', '子水'],
                6: ['辰土', '午火', '申金', '戌土', '子水', '寅木'],
                7: ['未土', '巳火', '卯木', '丑土', '亥水', '酉金']
        } # 存储地支五行
        self.yao_wuxing = [] # 存储六爻的地支五行
        for i in range(6):
            if i <= 2:
                self.yao_wuxing.append( wxs[self.num[1]][i] )
            else:
                self.yao_wuxing.append( wxs[self.num[0]][i] )

    def deco_liuqin(self):
        """六爻的六亲"""
        self.liu_qin = [] # 存储六爻的六亲
        for i in range(6):
            wx1 = self.yao_wuxing[i][1]
            step = WuXing().relation(self.wu_xing, wx1)
            self.liu_qin.append( LiuQin().index(step) )

    def write_content(self, flag=1):
        """写入内容，flag为是否加上世应"""
        self.content = [] # 按从上到下存储各爻内容
        for i in range(6):
            info = f'\t{self.liu_qin[i]}{self.yao_wuxing[i]}  {self.yaos[i].image}    '
            if flag:
                if i == self.shi_ying[0]:
                    info += '世 \t'
                elif i == self.shi_ying[1]:
                    info += '应 \t'

            self.content.append(info)

class GuaChange():
    """卦变"""
    def __init__(self, yaos):
        self.old_gua = Gua64(yaos)

        self.new_yaos, self.move_id = [], []
        for i in range(6):
            yao = copy.copy(yaos[i])
            if yao.num in [6, 9]: self.move_id.append(i)
            yao.change()
            self.new_yaos.append(yao)

        self.new_gua = Gua64(self.new_yaos)
        self.new_gua.wu_xing = self.old_gua.wu_xing # 使用原卦五行
        self.new_gua.deco_liuqin()
        self.new_gua.write_content((0)) # 改变五行后重写六亲及内容

    def disp(self):
        """格式化输出卦名及内容"""
        # 输出卦名
        if self.move_id:
            print(self.old_gua.long_name, self.new_gua.long_name)
        else:
            print(self.old_gua.long_name)
        # 输出内容
        for i in range(5, -1, -1):
            info = self.old_gua.content[i]
            if i in self.move_id: info += self.new_gua.content[i]

            print(info)




""" import random as r
gua = Gua64([Yao(r.randint(6, 9)) for i in range(6)])
print(gua.name)
print(gua.gong)
print(gua.wu_xing) """

"""
后续改进：
将卦名及八宫存放到外部文件中。
"""