from functools import partial
from UI.mainUI import Main
from UI.addEditCoffeeForm import DialogForm
from PyQt5 import uic, QtWidgets
import sys
import sqlite3


class Dialog(DialogForm):
    def __init__(self):
        super().__init__()

    def show(self, set_default=False):
        if set_default:
            self.radioButton.setChecked(True)
            self.roast_field.setValue(0.5)
            self.price_field.setValue(300.0)
            self.package_size_field.setValue(500.0)
        super().show()

    def get_params(self):
        variety_name = self.variety_field.text()
        roast_degree = self.roast_field.value()
        is_mashed = int(self.radioButton.isChecked())
        taste_desc = self.taste_desc_field.text()
        price = self.price_field.value()
        package_size = self.package_size_field.value()
        if variety_name and taste_desc:
            return {"ID": None,
                    "variety_name": variety_name,
                    "roast_degree": roast_degree,
                    "is_mashed": is_mashed,
                    "taste_desc": taste_desc,
                    "price": price,
                    "package_size": package_size
                    }

    def closeEvent(self, event):
        self.variety_field.setText("")
        self.taste_desc_field.setText("")
        event.accept()

    def fill(self, record):
        id_, variety_name, roast_degree, is_mashed, taste_desc, price, package_size = record
        self.variety_field.setText(variety_name)
        self.roast_field.setValue(roast_degree)
        if is_mashed == 1:
            self.radioButton.setChecked(True)
        elif is_mashed == 0:
            self.radioButton_2.setChecked(True)
        self.taste_desc_field.setText(taste_desc)
        self.price_field.setValue(price)
        self.package_size_field.setValue(package_size)


class MainWindow(Main):
    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.dialog = Dialog()
        self.create_database()
        self.fill_table()
        self.add_button.clicked.connect(partial(self.show_dialog, 0))
        self.edit_button.clicked.connect(partial(self.show_dialog, 1))
        self.row = 0

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

    def show_dialog(self, index: int):
        if index == 0:
            self.dialog.ok_button.clicked.connect(self.add_record)
            self.dialog.show(set_default=True)
        elif index == 1 and (row := self.table.currentRow()) != -1:
            self.dialog.ok_button.clicked.connect(self.update_record)
            record = self.conn.execute(
                "SELECT * FROM items WHERE ID = ?", (row + 1,)).fetchone()
            self.dialog.fill(record)
            self.row = row + 1
            self.dialog.show()

    def add_record(self):
        if (data := self.dialog.get_params()) is not None:
            self.dialog.close()
            self.conn.execute("""INSERT INTO items VALUES (
                :ID, :variety_name, :roast_degree, :is_mashed, :taste_desc,
                :price, :package_size)""", data)
            self.conn.commit()
            self.fill_table()

    def update_record(self):
        if (data := self.dialog.get_params()) is not None:
            self.dialog.close()
            data["ID"] = self.row
            self.conn.execute("""UPDATE items SET
                variety_name = :variety_name,
                roast_degree = :roast_degree,
                is_mashed = :is_mashed,
                taste_desc = :taste_desc,
                price = :price,
                package_size = :package_size
                WHERE ID = :ID
            """, data)
            self.conn.commit()
            self.fill_table()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow("data/coffee.sqlite")
    window.show()
    sys.exit(app.exec())
