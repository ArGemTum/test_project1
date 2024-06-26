import sys
import random
import string
import io
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QFont


class CaptchaApp(QWidget):
    def __init__(self, main_app_callback):
        """
        Инициализирует виджет CAPTCHA и устанавливает функцию обратного вызова для основного приложения.
        """
        super().__init__()
        self.main_app_callback = main_app_callback
        self.initUI()

    def initUI(self):
        """
        Инициализирует пользовательский интерфейс для CAPTCHA и авторизации.
        """
        self.setWindowTitle('Авторизация')

        font = QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(11)
        self.login_label = QLabel('Логин', self)
        self.login_entry = QLineEdit(self)
        self.login_label.setFont(font)

        self.password_label = QLabel('Пароль', self)
        self.password_label.setFont(font)
        self.password_entry = QLineEdit(self)
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.captcha_label = QLabel('Введите каптчу', self)
        self.captcha_label.setFont(font)
        self.captcha_entry = QLineEdit(self)

        self.captcha_image_label = QLabel(self)

        self.refresh_button = QPushButton('Обновить каптчу', self)
        self.refresh_button.setFont(font)
        self.refresh_button.clicked.connect(self.generate_captcha)

        self.submit_button = QPushButton('Войти', self)
        self.submit_button.setFont(font)
        self.submit_button.clicked.connect(self.validate)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.captcha_label)
        layout.addWidget(self.captcha_entry)
        layout.addWidget(self.captcha_image_label)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        self.generate_captcha()

    def generate_captcha(self):
        """
        Генерирует случайный CAPTCHA текст, создает изображение CAPTCHA и отображает его в интерфейсе.
        """
        self.captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        image = Image.new('RGB', (210, 50), (255, 255, 255))
        font = ImageFont.truetype("arial.ttf", 36)
        draw = ImageDraw.Draw(image)
        draw.text((10, 5), self.captcha_text, font=font, fill=(0, 0, 0))

        # Добавление зачеркивания символов
        for char in self.captcha_text:
            x = random.randint(0, 150)
            y = random.randint(0, 50)
            x_end = x + random.randint(10, 20)
            y_end = y + random.randint(-10, 10)
            draw.line([(x, y), (x_end, y_end)], fill=(0, 0, 0), width=3)

        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        byte_arr.seek(0)
        qimage = QImage()
        qimage.loadFromData(byte_arr.read())

        self.captcha_image = QPixmap.fromImage(qimage)
        self.captcha_image_label.setPixmap(self.captcha_image)

    def validate(self):
        """
        Проверяет правильность введенных пользователем данных (логин, пароль и CAPTCHA).
        Если данные корректны, скрывает виджет CAPTCHA и запускает основное приложение.
        Если данные некорректны, показывает сообщение об ошибке.

        Логин и пароль для проверки установлены жестко (login: "123", password: "123").
        """
        login = self.login_entry.text()
        password = self.password_entry.text()
        captcha_input = self.captcha_entry.text()

        if login != "123" or password != "123":
            QMessageBox.critical(self, 'Error', 'Please enter the correct login and password.')
        elif captcha_input != self.captcha_text:
            QMessageBox.critical(self, 'Error', 'Captcha does not match.')
            self.generate_captcha()
        else:
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.hide()
            self.main_app_callback()
