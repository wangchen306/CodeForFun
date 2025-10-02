# 导入程序运行必须模块
import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
# 导入designer工具生成的login模块
from sentenceUI import Ui_Form
import pickle
from sentence import Sentence


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.queryBtn.clicked.connect(self.showQueryResult)
        self.addItemBtn.clicked.connect(self.newItem)
        self.addRowBtn.clicked.connect(self.newRow)
        self.delRowBtn.clicked.connect(self.delRow)

        self.examples = self.load()
        self.allEmb = self.updateEmb()

    def showQueryResult(self):
        result = []
        emb = self.embeddingCbBox.currentText()
        for sentence in self.examples:
            if emb in sentence.embedding:
                result.append(sentence)

        self.display(result)
        self.adviceLabel.setText(f'筛选完成，共{len(result)}个结果')

    def display(self, lst):
        num_items = len(lst)

        self.infoTable.setRowCount(num_items + 1)
        self.setTableTitle()

        for id, sentence in enumerate(lst):
            self.infoTable.setItem(id+1, 0, QTableWidgetItem(sentence.jpn))
            self.infoTable.setItem(id+1, 1, QTableWidgetItem(','.join(sentence.embedding)))
            self.infoTable.setItem(id+1, 2, QTableWidgetItem(sentence.where))
            self.infoTable.setItem(id+1, 3, QTableWidgetItem(sentence.chn))

    def newRow(self):
        self.infoTable.setRowCount(self.infoTable.rowCount() + 1)
        self.adviceLabel.setText(f'已新增一行，请输入内容')

    def newItem(self):
        num_items = self.infoTable.rowCount() - 1
        new_example = []
        for row in range(1, num_items + 1):
            try:
                jpn = self.infoTable.item(row, 0).text()
                emb = self.infoTable.item(row, 1).text().split(',')
                where = self.infoTable.item(row, 2).text()
                chn = self.infoTable.item(row, 3).text()
                sentence = Sentence(jpn, chn, emb, where)
                new_example.append(sentence)
            except AttributeError:
                break
        self.examples.extend(new_example)
        self.save()
        self.updateEmb()

        self.adviceLabel.setText(f'已将{num_items}个条目添加到库中')

    def delRow(self):
        selected_item = self.infoTable.currentItem()  # 获取当前选中的单元格
        row = selected_item.row()
        if selected_item:
            for id, sentence in enumerate(self.examples):
                if sentence.jpn == self.infoTable.item(row, 0).text():
                    self.examples.pop(id)
                    break

        self.display(self.examples)
        self.save()
        self.updateEmb()
        self.adviceLabel.setText(f'删除成功')

    def load(self):
        try:
            with open(f'./data.bin', 'rb') as file:
                examples = pickle.load(file)
        except FileNotFoundError:
            examples = []

        return examples

    def save(self):
        with open('./data.bin', 'wb') as file:
            pickle.dump(self.examples, file)

    def updateEmb(self):
        allEmb = []
        for sentence in self.examples:
            allEmb.extend(sentence.embedding)
        allEmb = list(set(allEmb))

        self.updateEmbCbBox(allEmb)

        return allEmb


if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
