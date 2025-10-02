from 序列 import DiZhi as DZ, HunTianJiaZi as HTJZ
import math as m
import datetime as dtm

def trim0(lst):
    """去除首位的0，返回列表"""
    newlst = []
    for i in lst:
        while i[0] == '0':
            i = i[1: ]
        newlst.append(i)
    return newlst

class Date:
    """表示公历日期与干支日期"""
    def __init__(self, date):
        dates = trim0(date.split('/'))
        self.year, self.nian = eval(dates[0]), '甲子'
        self.month, self.yue = eval(dates[1]), '子'
        self.day, self.ri = eval(dates[2]), '甲子'

        self.dzs = DZ(); self.jzs = HTJZ()

        self.monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # 月份天数
        global jieqis, F_jieqis
        jieqis = ['小寒', '立春', '惊蛰', '清明', '立夏', '芒种', '小暑', '立秋', '白露', '寒露', '立冬', '大雪']
        F_jieqis = [365.242 * (self.year-1900) + 6.2 + 15.22 * x - 1.9 * m.sin(0.262 * x) for x in range(0, 24, 2)]
        # 置闰
        flag1 = (not self.year%100) and (self.year%4); flag2 = self.year%400
        if flag1 and flag2: self.monthdays[1] = 29
        
        self.year2nian(); self.month2yue(); self.day2ri()
        self.xunkong = self.jzs.xunkong(self.ri)[1]
        self.make_info()

        

    def year2nian(self):
        """将年转换为年干支"""
        yearnum = (self.year - 3) % 60
        self.nian = self.jzs.index(yearnum)

    def month2yue(self):
        """转换为月支"""
        delta = dtm.datetime.strptime(f'{self.year}-{self.month}-{self.day}', '%Y-%m-%d') -\
                dtm.datetime.strptime('1900-1-1', '%Y-%m-%d')
        F_day = delta.days + 1
        for i in range(len(jieqis)-1):
            if F_jieqis[i] <= F_day and F_jieqis[i+1] > F_day:
                self.yue = self.dzs.index(i+2) # 如果没有修改则为最后一个月，即初始化的子月

    def day2ri(self):
        """转换为日干支"""
        daynum = (self.year-1900+3)*5 + 55 \
                + (self.year-1900-1)//4 \
                + sum(self.monthdays[: self.month-1]) + self.day
        self.ri = self.jzs.index(daynum % 60)

    def make_info(self):
        """生成日期语句"""
        self.gz_info = f'\t干支历：{self.nian}年 {self.yue}月 {self.ri}日 旬空：{self.xunkong}'
        self.sl_info = f'\t公历：    {self.year}年{self.month}月{self.day}日'

    def disp(self):
        """格式化输出整个日期"""
        print('Warning：月支计算可能有误差！')
        print(self.sl_info)
        print(self.gz_info)
        print('旬空：', self.xunkong)

    def get_nian(self):
        """返回年干"""
        return self.nian

    def get_yue(self):
        """返回月干"""
        return self.yue

    def get_ri(self):
        """返回日干"""
        return self.ri

    def get_all(self, flag=1):
        """返回日期语句，flag为1输出干支历，为0输出公历"""
        return self.gz_info if flag else self.sl_info

""" date = Date('2018/3/28')
date.disp() """