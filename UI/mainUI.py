from PyQt5 import QtWidgets


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(800, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.edit_button = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.edit_button)
        self.add_button = QtWidgets.QPushButton(self)
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.setWindowTitle("Эспрессо")
        self.edit_button.setText("Редактировать")
        self.add_button.setText("Добавить")
