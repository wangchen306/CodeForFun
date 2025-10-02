import re

class StrIndex:
    """一组元素的序数"""
    def __init__(self, container):
        self.__container = container
        self.__nums = len(self.__container)

    def getvalue(self):
        """返回所有元素"""
        return self.__container

    def getnums(self):
        """返回元素个数"""
        return self.__nums

    
    def index(self, input):
        """若输入序数，返回对应元素；输入元素值，返回对应序数（首位为1）"""
        if isinstance(input, str):
            if input in self.__container:
                return self.__container.index(input) + 1
            else:
                return None
        elif isinstance(input, int):
            return self.__container[input-1] if input <= self.__nums else None
        else:
            return None

    def next(self, value, step):
        """查找之后step位的元素值"""
        if value in self.__container:
            val_id = self.__container.index(value)
            new_id = (val_id + step) % self.__nums
            return self.__container[new_id]
        else:
            return None

class TianGan(StrIndex):
    """十天干"""
    def __init__(self):
        super().__init__('甲乙丙丁戊己庚辛壬癸')

class DiZhi(StrIndex):
    """十二地支"""
    def __init__(self):
        self.dizhi = '子丑寅卯辰巳午未申酉戌亥'
        self.wuxing = '水土木木土火火土金金土水'
        super().__init__('子丑寅卯辰巳午未申酉戌亥')

    def get_wuxing(self, dz):
        """返回地支对应的五行"""
        return self.wuxing[self.dizhi.index(dz)] if dz in self.dizhi else None

class HunTianJiaZi(StrIndex):
    """六十浑天甲子"""
    def __init__(self):
        self.generate()
        # 创建甲子对象
        super().__init__(self.jzs)

        # 六十旬
        self.xuns = self.Xuns()

    def generate(self):
        """生成六十甲子"""
        self.tgs = TianGan()
        self.dzs = DiZhi()
        """ self.jzs = [] # 存储六十甲子
        tg, dz = '甲', '子'
        while tg != '癸' or dz != '亥':
            self.jzs.append(tg + dz)
            tg, dz = self.tgs.next(tg, 1), self.dzs.next(dz, 1)

        self.jzs.append(tg + dz) """
        self.jzs = [self.tgs.index(i%10)+self.dzs.index(i%12) for i in range(1, 61)]


    def Xuns(self):
        """生成六十旬"""
        xuns = {}# 存储各个旬及其旬空,value为列表，前十项为旬，最后一项为旬空

        # 查找各个旬首
        pattern = r'甲.'
        starts = re.findall(pattern, ''.join(self.jzs))

        # 生成每个旬
        for i in starts:
            id = self.jzs.index(i)
            xuns[i] = self.jzs[id: id+10]

            # 使用集合可以快速查找旬空，但返回值是按ASCII顺序的，需要处理
            empty_set = set(self.dzs.getvalue()) - set(''.join(xuns[i])[1::2])
            empty_str = ''.join(empty_set)
            if self.dzs.index(empty_str[0]) > self.dzs.index(empty_str[1]):
                empty_str = empty_str[::-1]
            xuns[i].append(''.join(empty_str))

        return xuns

    def xunkong(self, jiazi):
        """返回甲子所在的旬及其旬空"""
        for k, v in self.xuns.items():
            if jiazi in v:
                return (k, v[-1])

class WuXing(StrIndex):
    """五行"""
    def __init__(self):
        super().__init__('金水木火土')

    def relation(self, wx1, wx2):
        """输入五行，返回生克关系

        Args:
            wx1 (str): 五行1
            wx2 (str): 五行2

        Returns:
            [int]: 0, 1, -1, 2, -2
        """
        id1, id2 = self.index(wx1), self.index(wx2)
        return id2 - id1


class LiuQin(StrIndex):
    """六亲"""
    def __init__(self):
        super().__init__(['兄弟', '子孙', '妻财','官鬼', '父母'])

    def index(self, input):
        """输入位置，返回元素

        Args:
            input (int): 0, 1, -1, 2, -2

        Returns:
            [str]: 对应位置的六亲
        """
        return super().index(input+1)

class LiuShou(StrIndex):
    """六兽"""
    def __init__(self):
        super().__init__(['青龙', '朱雀', '勾陈', '腾蛇', '白虎', '玄武'])
        self.rigan = ['甲乙', '丙丁', '戊', '己', '庚辛', '壬癸']

    def turns(self, rg):
        """输入日干，返回六兽顺序"""
        # 查找起始位置
        for i in range(6):
            if rg in self.rigan[i]:
                id = i
                break

        # 生成六兽顺序
        return [self.index((id+ii)%6+1) for ii in range(6)]


""" tg = HunTianJiaZi()
print(tg.index('丁卯')) """