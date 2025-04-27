import json
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QListWidget,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QSpinBox,
    QDoubleSpinBox,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt


class InitWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Инициализация")
        self.setMinimumSize(600, 400)

        # Список для хранения рейсов и их последующей записи в JSON-файл
        self.flights = []

        self.main_layout = QVBoxLayout()

        welcome_container = QHBoxLayout()
        welcome_container.addStretch()
        self.welcome_label = QLabel(
            "Здравствуйте, для продолжения вам необходимо указать максимальный общий вес багажа для каждого нужного вам рейса"
        )
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setMinimumWidth(400)
        self.welcome_label.setMaximumWidth(500)
        welcome_container.addWidget(self.welcome_label)
        welcome_container.addStretch()
        self.main_layout.addLayout(welcome_container)

        self.main_layout.addSpacing(50)

        self.flight_layout = QHBoxLayout()

        self.flight_info_layout = QVBoxLayout()
        self.flight_info_layout.setSpacing(5)  # Уменьшаем расстояние между элементами

        self.flight_number_layout = QHBoxLayout()
        self.flight_number_label = QLabel("Номер рейса")
        self.flight_number_input = QSpinBox()
        self.flight_number_input.setMinimum(1)
        self.flight_number_layout.addWidget(self.flight_number_label)
        self.flight_number_layout.addWidget(self.flight_number_input)
        self.flight_info_layout.addLayout(self.flight_number_layout)

        self.max_weight_layout = QHBoxLayout()
        self.max_weight_label = QLabel("Максимальный вес багажа")
        self.max_weight_input = QDoubleSpinBox()
        self.max_weight_input.setMinimum(0.1)
        self.max_weight_input.setMaximum(1000.0)
        self.max_weight_layout.addWidget(self.max_weight_label)
        self.max_weight_layout.addWidget(self.max_weight_input)
        self.flight_info_layout.addLayout(self.max_weight_layout)

        self.accept_flight_info_button = QPushButton("Добавить рейс")
        self.flight_info_layout.addWidget(self.accept_flight_info_button)
        self.accept_flight_info_button.clicked.connect(self.add_flight_to_list)

        self.flight_layout.addLayout(self.flight_info_layout)

        self.flights_list = QListWidget()
        self.flight_layout.addWidget(self.flights_list)

        self.main_layout.addLayout(self.flight_layout)

        spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.main_layout.addItem(spacer)

        confirm_layout = QHBoxLayout()
        self.accept_button = QPushButton("Подтвердить")
        self.accept_button.setFixedWidth(200)
        self.accept_button.setMinimumHeight(40)
        confirm_layout.addStretch()
        confirm_layout.addWidget(self.accept_button)
        confirm_layout.addStretch()
        self.main_layout.addLayout(confirm_layout)

        spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )
        self.main_layout.addItem(spacer)

        self.setLayout(self.main_layout)

        self.accept_button.clicked.connect(self.on_accept_clicked)

    def add_flight_to_list(self):
        flight_number = self.flight_number_input.value()
        max_weight = self.max_weight_input.value()

        for flight in self.flights:
            if flight["flight_number"] == flight_number:
                self.show_error_message("Рейс с таким номером уже существует!")
                return

        flight_info = (
            f"\nНомер рейса: {flight_number}\nМаксимальный вес: {max_weight} кг\n"
        )
        flight = QListWidgetItem(flight_info)

        flight_data = {
            "flight_number": flight_number,
            "max_weight": max_weight,
        }

        self.flights_list.addItem(flight)
        self.flights.append(flight_data)

        # Clear inputs
        self.flight_number_input.setValue(self.flight_number_input.minimum())
        self.max_weight_input.setValue(self.max_weight_input.minimum())

    def save_max_weights_to_json(self, filename):
        with open(filename, "w", encoding="UTF-8") as f:
            json.dump(self.flights, f, ensure_ascii=False, indent=4)
        return True

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def on_accept_clicked(self):
        if not self.flights:
            self.close()
            return

        self.save_max_weights_to_json("max_weights.json")
        self.close()
