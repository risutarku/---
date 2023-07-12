from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, \
     QLabel, QLineEdit
import sys
import random

#  поиск разрешающего элемента
def findMin(matrix):
    m = matrix[0][0]
    ind = []
    for i in range(len(matrix) - 1):
        el = matrix[i][-1]
        for j in range(len(matrix[i]) - 1):
            if el / matrix[i][j] and ((el > 0 and matrix[i][j] > 0) or (el < 0 and matrix[i][j] < 0)) < m:
                m = matrix[i][j]
                ind = [i, j]
    return ind


def zapolnenie(matrix, razreshElem):
    newElem = matrix[razreshElem[0]][razreshElem[1]]
    newMatrix = []
    #  заполняем разрешаюший столбец и строку
    for i in range(len(matrix)):
        line = []
        for j in range(len(matrix[i])):
            if (i == razreshElem[0] and j != razreshElem[1]) or (j == razreshElem[1] and i != razreshElem[1]):
                if i == razreshElem[0]:
                    line.append(matrix[i][j] * newElem ** -1)
                else:
                    line.append(-matrix[i][j] * newElem ** -1)
            elif i == razreshElem[0] and j == razreshElem[j]:
                line.append(newElem ** -1)
            else:
                line.append(0)
        newMatrix.append(line)
    #  заполняем остальные элементы методом Штифеля
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if newMatrix[i][j] == 0:
                newMatrix[i][j] = (matrix[i][j] * newElem - matrix[i][razreshElem[1]] * matrix[razreshElem[0]][j]) \
                                  / newElem
    return newMatrix

class MatrixGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Генератор матрицы"
        self.width = 1000
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)

        self.rowsInput = QLineEdit(self)
        self.rowsInput.setGeometry(40, 30, 50, 20)
        self.rowsInput.setPlaceholderText('Количество строк')

        self.colsInput = QLineEdit(self)
        self.colsInput.setGeometry(110, 30, 50, 20)
        self.colsInput.setPlaceholderText('Количество столбцов')

        self.oporniyTable = QTableWidget(self)
        self.oporniyTable.setGeometry(40, 60, 450, 180)

        self.resultTable = QTableWidget(self)
        self.resultTable.setGeometry(40, 400, 450, 180)

        self.generateBtn = QPushButton('Сгенерировать', self)
        self.generateBtn.setGeometry(40, 270, 140, 20)
        self.generateBtn.clicked.connect(self.generateMatrix)

        self.readBtn = QPushButton('Расчитать', self)
        self.readBtn.setGeometry(40, 610, 140, 20)
        self.readBtn.clicked.connect(self.stifelMethod)

    def generateMatrix(self):
        rows = int(self.rowsInput.text())
        cols = int(self.colsInput.text())
        self.oporniyTable.setRowCount(rows)
        self.oporniyTable.setColumnCount(cols)

        for i in range(rows):
            for j in range(cols):
                value = random.randint(1, 100)
                #  item = QTableWidgetItem(str(value))
                #  self.resultTable.setItem(i, j, item)

    def stifelMethod(self):
        #  считываем матрицу из таблицы
        matrix = []
        for i in range(self.oporniyTable.rowCount()):
            line = []
            for j in range(self.oporniyTable.columnCount()):
                if i != self.oporniyTable.rowCount() - 1:
                    line.append(int(str(self.oporniyTable.item(i, j).text())))
                else:
                    line.append(-int(str(self.oporniyTable.item(i, j).text())))
            matrix.append(line)
        razreshElem = findMin(matrix)

        newMatrix = zapolnenie(matrix, razreshElem)
        print(newMatrix)
        positions = []
        for i in range(len(matrix) - 1):
            positions.append(1)
        print(positions)
        for i in range(len(positions)):
                if positions[i] == 0:
                    positions[i] = 1
                elif positions[i] == 1:
                    positions[i] = 0
        newRazreshElem = positions
        print(newRazreshElem)
        answer = zapolnenie(newMatrix, newRazreshElem)
        for i in range(len(answer)):
            for j in range(len(answer[i])):
                answer[i][j] = round(answer[i][j], 3)
        print(answer)
        rows = int(self.rowsInput.text())
        cols = int(self.colsInput.text())
        self.resultTable.setRowCount(rows)
        self.resultTable.setColumnCount(cols)
        for i in range(len(answer)):
            for j in range(len(answer[i])):
                it = QTableWidgetItem(str(answer[i][j]))
                self.resultTable.setItem(i, j, it)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixGenerator()
    window.show()
    sys.exit(app.exec_())