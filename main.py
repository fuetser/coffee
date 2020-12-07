from PyQt5 import uic, QtWidgets
import sys
import sqlite3


class MainWindow(QtWidgets.QWidget):
    def __init__(self, db_name):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_database()
        self.fill_table()

    def create_database(self):
        self.conn.execute("""CREATE TABLE IF NOT EXISTS items(
                ID INTEGER PRIMARY KEY,
                variety_name TEXT,
                roast_degree REAL,
                is_mashed INTEGER,
                taste_desc TEXT,
                price REAL,
                package_size REAL
            )
        """)
        self.conn.commit()

    def fill_database(self):
        self.conn.execute("""INSERT INTO items VALUES
            (1, 'Арабика', 0.5, 1, 'Отличается сложным ароматом', 350.5, 500.0),
            (2, 'Робуста', 0.3, 0, 'Высокое содержание кофеина', 450.9, 350.0),
            (3, 'Либерика', 0.7, 0, 'Используется в смесях', 300.68, 450.5),
            (4, 'Эксцельза', 0.9, 1, 'Не имеет хозяйственного значения', 200.0, 200.0),
            (5, 'Арабика Сантос', 0.4, 0, 'Терпкий, с легкой горчинкой', 400.0, 300.0),
            (6, 'Арабика Медельин', 0.5, 1, 'Мягкий вкус со сладковатым оттенком', 350.0, 300.5),
            (7, 'Арабиен Мокко', 0.8, 0, 'Винный привкус, высокая кислотность', 450.0, 200.0)
        """)
        self.conn.commit()

    def fill_table(self):
        table_data = self.conn.execute("SELECT * FROM items").fetchall()
        headers = ("ID", "Название сорта", "Степень обжарки",
            "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки")
        self.table.setRowCount(0)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        for i, row in enumerate(table_data):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow("coffee.sqlite")
    window.show()
    sys.exit(app.exec())
