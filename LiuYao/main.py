from 卦 import *
from 干支纪历 import *

print()
date = Date('2021/9/27')
date.disp()

numbers = [7, 8, 8, 7, 8, 7]
yaos = [Yao(numbers[i]) for i in range(6)]
gua = GuaChange(yaos)
gua.disp()
print()