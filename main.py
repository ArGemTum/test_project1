import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from MainMenu import Ui_MainMenu
from DataBaseView import Ui_DataBaseView
from captha import CaptchaApp
import psycopg2

def close():
    """
    Выход из приложения.
    """
    sys.exit()

def back():
    """
    Возвращает к главному меню и закрывает окна просмотра базы данных.
    """
    MainMenu.show()
    DataBaseView.close()

def connect_to_db(ui_dbview):
    """
    Подключает к базе данных PostgreSQL и отображает данных выбранной таблицы.

    Действия:
    - Устанавливает параметры подключения к PostgreSQL (hostname, database, username, password, port).
    - Получает имя выбранной таблицы из выпадающего списка.
    - Пытается установить соединение с базой данных и выполнить SQL-запрос для получения данных из выбранной таблицы.
    - Отображает полученные данные в виде таблицы в интерфейсе окна просмотра базы данных.
    - В случае ошибки выводит сообщение об ошибке с деталями.

    Замечания:
    - Для подключения к базе данных используется модуль psycopg2.
    """
    hostname = 'localhost'
    database = 'postgres'
    username = 'postgres'
    password = 'argemtum'
    port = 5432

    # Вспомогательная переменная, позволяющая выбирать необходимую таблицу из базы данных
    selected_table = ui_dbview.choose_db_table.currentText()

    try:
        connection = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=password,
            port=port
        )
        QtWidgets.QMessageBox.information(None, "Успех", "Соединение с PostgreSQL успешно установлено")

        cursor = connection.cursor()
        query = f'SELECT * FROM fishing."{selected_table}"'
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        # Создание модели данных для отображения в таблице
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(columns)

        for row in rows:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)

        ui_dbview.db_viewer.setModel(model)

        cursor.close()
        connection.close()

    except Exception as error:
        QtWidgets.QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к PostgreSQL: {error}")

def go_to_view_db():
    """
    Отображает окно просмотра базы данных путем переключения на него из главного меню.

    Действия:
    - Подключает обработчики событий для кнопок возврата к главному меню и подключения к базе данных.
    - Заполняет выпадающий список таблицами базы данных для выбора пользователем.
    """
    global DataBaseView
    DataBaseView = QtWidgets.QWidget()
    DataBaseView.setFixedSize(1400, 800)
    ui_dbview = Ui_DataBaseView()
    ui_dbview.setupUi(DataBaseView)
    DataBaseView.show()
    MainMenu.close()
    ui_dbview.go_back.clicked.connect(back)
    ui_dbview.try_to_connect_db.clicked.connect(lambda: connect_to_db(ui_dbview))

    tables = ["User", "Order", "Product", "OrderProduct", "Adress", "Role"]
    ui_dbview.choose_db_table.addItems(tables)

# Вывод CAPTCHA, главного меню и второстепенных окон производится в отдельно созданном файле, с целью структурирования кода.
# Такой подход позволяет сделать код более организованным и читабельным.
def show_main_app():
    """
    Отображает основное окно приложения.

    Действия:
    - Устанавливает обработчики событий для кнопок выхода из приложения и перехода к просмотру базы данных.
    """
    global MainMenu
    MainMenu = QtWidgets.QMainWindow()
    MainMenu.setFixedSize(1400, 800)
    ui_main = Ui_MainMenu()
    ui_main.setupUi(MainMenu)
    MainMenu.show()

    ui_main.exit_application.clicked.connect(close)
    ui_main.go_to_database.clicked.connect(go_to_view_db)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    captcha = CaptchaApp(show_main_app)
    captcha.setFixedSize(230, 300)
    captcha.show()
    sys.exit(app.exec_())
