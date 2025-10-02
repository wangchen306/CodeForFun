import tkinter as tk
from tkinter import ttk
import 干支纪历 as GZL
import 卦 as GUA
import re
import os; os.chdir(os.path.dirname(__file__))
from PIL import Image, ImageTk


global fontset
fontset = ('楷体', 14)

class App():
    def __init__(self, master):
        global x0, y0 # 起始位置
        x0, y0 = 0, 0

        self.create_frame1(master)
        self.create_frame2(master)
        self.create_frame3(master)


    def create_frame1(self, master):
        """第一个框架：日期"""
        self.frame1 = tk.Frame(master)
        self.frame1.grid(row=1, column=1, sticky='nsew', pady=10, padx=10)

        self.f1_l1 = tk.Label(self.frame1, text='输入日期', font=(16))
        self.f1_l1.grid(row=1, column=1)

        self.AutoAndManual()

        self.EnterDate()

        self.ShowDate()

    def ShowDate(self):
        """ 显示日期 """
        self.f1_l2 = tk.Label(self.frame1, text='', font=fontset)
        self.f1_l2.grid(row=4, column=2, columnspan=3, sticky='nsew')

    def EnterDate(self):
        """ 日期输入部分 """
        self.f1_e1 = tk.Entry(self.frame1, state='readonly')
        self.f1_e1.grid(row=2, column=3, padx=5)
        self.f1_fmt_lb = tk.Label(self.frame1, text='格式：2021/10/1')
        self.f1_fmt_lb.grid(row=2, column=5, padx=5)

        self.f1_b1 = tk.Button(self.frame1, text='确定',
                            command=self.f1_rb_click, state='disabled')
        self.f1_b1.grid(row=2, column=4, padx=5)

        self.f1_alert_lb = tk.Label(self.frame1, text='输入格式不符！')

    def AutoAndManual(self):
        """ 手动自动两个选项 """
        self.f1_var1 = tk.StringVar()
        self.f1_rb1 = tk.Radiobutton(self.frame1, text='手动输入',
                                    variable=self.f1_var1, value='M',
                                    command=self.f1_EnterDate)
        self.f1_rb1.grid(row=2, column=2, padx=5, pady=5)
        self.f1_rb2 = tk.Radiobutton(self.frame1, text='自动获取',
                                    variable=self.f1_var1, value='A',
                                    command=self.f1_rb_click)
        self.f1_rb2.grid(row=3, column=2)

    def f1_EnterDate(self):
        """选择手动输入，设置文本框可以输入"""
        self.f1_e1.config(state='normal')
        self.f1_b1.config(state='normal')

    def f1_rb_click(self):
        """生成日期"""
        # 确定日期
        if self.f1_var1.get() == 'A':
            # 自动获取，并设置文本框禁止输入，同时消除提示
            td = GZL.dtm.datetime.now().strftime(r'%Y/%m/%d')
            self.f1_e1.config(state='readonly')
            self.f1_b1.config(state='disabled')
            self.f1_alert_lb.grid_forget()
            self.f1_fmt_lb.config(fg='black')
            # 显示
            self.disp_date(td)
        elif self.f1_var1.get() == 'M':
            # 手动输入
            # 首先判断输入是否合法
            pattern = r'^\d{4}/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9])$'
            td = self.f1_e1.get()
            if re.fullmatch(pattern, td):
                # 如果匹配成功则显示，同时取消警告
                self.f1_alert_lb.grid_forget()
                self.f1_fmt_lb.config(fg='black')
                self.disp_date(td)
            else:
                # 不符则发出警告
                self.f1_alert_lb.grid(row=2, column=6)
                self.f1_fmt_lb.config(fg='red')

    def disp_date(self, td):
        # 拼接输出
        date = GZL.Date(td)
        sl_cd = date.get_all(0) # 阳历
        gzl = date.get_all(1) # 干支历
        self.f1_l2.config(text=sl_cd+'\n'+gzl)
        tk.Label(self.frame1, text='月柱的计算可能有误差！').grid(row=4, column=5, columnspan=2)

    def create_frame2(self, master):
        """第二个框架：点卦"""
        self.frame2 = tk.Frame(master)
        self.frame2.grid(row=2, column=1, sticky='nsew', pady=10, padx=10)

        self.f2_l1 = tk.Label(self.frame2, text='开始点卦', font=(16))
        self.f2_l1.grid(row=1, column=1)

        self.six_cbs()

        self.ConfirmButton()

        self.cal_numbers()

    def ConfirmButton(self):
        """ 确定按钮 """
        self.f2_b1 = tk.Button(self.frame2, text='开始输入', command=self.input_rst)
        self.f2_b1.grid(row=2, column=1)
        self.f2_b2 = tk.Button(self.frame2, text='输入完成', command=self.show_result)
        self.f2_b2.grid(row=2, column=2)

    def six_cbs(self):
        """六次结果"""
        self.f2_l2_names, self.f2_cb_names = [0]*6, [0]*6 # 存储六个标签和下拉框控件
        # 下拉框
        for i in range(6):
            self.f2_l2_names[i] = tk.Label(self.frame2, text=f'第{i+1}次：')
            self.f2_l2_names[i].grid(row=8-i, column=2)

            values = [f'{i}字面{3-i}背面' for i in range(4)]
            self.f2_cb_names[i] = ttk.Combobox(self.frame2, width=9, state='readonly',
                                values=values)
            self.f2_cb_names[i].current(0) # 指定默认值
            self.f2_cb_names[i].grid(row=8-i, column=3)

    def input_rst(self):
        """显示输入控件并擦除爻控件"""
        for i in range(6):
            self.f2_l2_names[i].grid(row=8-i, column=2)
            self.f2_cb_names[i].grid(row=8-i, column=3)
            # 擦除部件
            if getattr(self, 'name_lb', None): self.name_lb.grid_forget()
            if getattr(self, 'wl_lbs', None): self.wl_lbs[i].grid_forget()
            if getattr(self, 'yao_lbs', None): self.yao_lbs[i].grid_forget()
            if getattr(self, 'sy_lbs', None): self.sy_lbs[i].grid_forget()

            if getattr(self, 'arrow_lb', None): self.arrow_lb.grid_forget()
            if getattr(self, 'cgname_lb', None): self.cgname_lb.grid_forget()
            if getattr(self, 'cgwl_lbs', None): self.cgwl_lbs[i].grid_forget()
            if getattr(self, 'cgyao_lbs', None): self.cgyao_lbs[i].grid_forget()

    def show_result(self):
        """计算爻数并显示结果"""
        self.cal_numbers()

        global photos
        photos = []
        pto_names = ['老阴', '少阳', '少阴', '老阳']
        for name in pto_names:
            img = Image.open(f'images/{name}.png').resize((124,35))
            photos.append(ImageTk.PhotoImage(img))

        self.show_gua()

        if self.gua.move_id:
            # 如果卦变，则输出变卦内容
            self.show_change()

    def show_change(self):
        """显示变卦内容"""
        # 箭头
        self.arrow_lb = tk.Label(self.frame2, text='--->', font=fontset)
        self.arrow_lb.grid(row=5, column=8, padx=5)
        # 变卦名
        self.cgname_lb = tk.Label(self.frame2, text=self.gua.new_gua.long_name[2: ], font=fontset)
        self.cgname_lb.grid(row=2, column=11, columnspan=2, sticky='nsew')

        # 变卦内容
        self.cgwl_lbs, self.cgyao_lbs =\
                [0]*6, [0]*6 # 存储变卦各爻的五行六亲、爻像
        for i in range(6):
            self.cgwl_lbs[i] = tk.Label(self.frame2, font=fontset)
            self.cgyao_lbs[i] = tk.Label(self.frame2)
            if i in self.gua.move_id:
                self.cgwl_lbs[i].config(text=self.gua.new_gua.content[i][1: 5])
                self.cgyao_lbs[i].config(image=photos[self.gua.new_yaos[i].num-6])
            self.cgwl_lbs[i].grid(row=8-i, column=9, columnspan=2)
            self.cgyao_lbs[i].grid(row=8-i, column=11)

    def show_gua(self):
        """ 显示结果 """
        # 显示卦名
        self.show_name()
        # 显示卦象
        self.wl_lbs, self.yao_lbs, self.sy_lbs = [0]*6, [0]*6, [0]*6 # 存储六亲五行、爻像、世应
        for i in range(6):
            # 显示五行六亲
            self.wl_lbs[i] = tk.Label(
                self.frame2, font= fontset,
                text=self.gua.old_gua.content[i][1: 5])
            self.wl_lbs[i].grid(row=8-i, column=3, columnspan=2)
            # 显示爻像
            # self.yao_lbs[i] = tk.Label(self.frame2, text=self.yaos[i].state)
            self.yao_lbs[i] = tk.Label(self.frame2, image=photos[self.yaos[i].num-6])
            self.yao_lbs[i].grid(row=8-i, column=5, columnspan=2)
            # 显示世应
            if i == self.gua.old_gua.shi_ying[0]:
                sy_text = '世'
            elif i == self.gua.old_gua.shi_ying[1]:
                sy_text = '应'
            else:
                sy_text = ''
            self.sy_lbs[i] = tk.Label(self.frame2, text=sy_text, font=fontset)
            self.sy_lbs[i].grid(row=8-i, column=7, padx=5)

    def show_name(self):
        """显示原卦名"""
        self.name_lb = tk.Label(self.frame2, text=self.gua.old_gua.long_name[2: ], font=fontset)
        self.name_lb.grid(row=2, column=5, columnspan=2, sticky='nesw')

    def cal_numbers(self):
        """计算爻数并擦除输入控件，创建卦对象"""
        self.numbers = []
        for i in range(6):
            rst = self.f2_cb_names[i].get()
            self.numbers.append( eval(f'{rst[0]}*2+{rst[3]}*3') )
            self.f2_cb_names[i].grid_forget()
            self.f2_l2_names[i].grid_forget()

        self.yaos = [GUA.Yao(self.numbers[i]) for i in range(6)]
        self.gua = GUA.GuaChange(self.yaos)


    def create_frame3(self, master):
        """第三个框架：退出、重启等功能"""
        self.frame3 = tk.Frame(master)
        self.frame3.grid(column=1, row=3, sticky='nsew', pady=10, padx=10)

        self.f3_b1 = tk.Button(self.frame3, text='退出', command=self.frame3.quit, bg='red')
        self.f3_b1.grid(column=1, row=1)




win = tk.Tk()
app = App(win)
win.mainloop()