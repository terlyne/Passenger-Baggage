from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QLineEdit,
    QListWidget,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QDateTimeEdit,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QDateEdit,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
import json

from models.passenger import Passenger
from models.baggage import Baggage

from ui.init_widget import InitWidget


class MainWindow(QMainWindow):
    def __init__(self, Baggage: Baggage):
        super().__init__()
        self.Baggage = Baggage

        # Устанавливаем размер и заголовок окна
        self.setMinimumSize(700, 500)
        self.setWindowTitle("Ведение информации о багажах")

        # Создаем стек виджетов для переключения между экранами
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создаем основной layout
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Создаем контейнер для InitWidget
        self.init_container = QWidget()
        init_container_layout = QVBoxLayout()
        self.init_container.setLayout(init_container_layout)

        # Создаем InitWidget
        self.init_widget = InitWidget()
        init_container_layout.addWidget(self.init_widget)

        # Добавляем контейнер в главный layout
        self.main_layout.addWidget(self.init_container)

        # Создаем контейнер для основного интерфейса (пока скрытый)
        self.content_container = QWidget()
        self.content_container.hide()
        self.content_layout = QVBoxLayout()
        self.content_container.setLayout(self.content_layout)
        self.main_layout.addWidget(self.content_container)

        # Подключаем сигнал кнопки подтверждения
        self.init_widget.accept_button.clicked.connect(self.on_init_accepted)

        # Словарь для хранения текущего веса багажа по рейсам
        self.current_weights = {}

    def on_init_accepted(self):
        # Сохраняем данные о рейсах (даже если их нет)
        if not self.init_widget.save_max_weights_to_json("max_weights.json"):
            return

        # Скрываем init_container
        self.init_container.hide()

        # Инициализируем основной интерфейс
        self.init_main_window()

        # Показываем основной интерфейс
        self.content_container.show()

    def init_main_window(self):
        # Создаем layout для информации
        self.info_layout = QHBoxLayout()

        # Создаем разделы интерфейса
        self.draw_passenger_info_layout()
        self.draw_Baggage_info_layout()

        # Добавляем разделы в info_layout
        self.info_layout.addLayout(self.passenger_info_layout)
        self.info_layout.addLayout(self.Baggage_info_layout)

        # Добавляем info_layout в content_layout
        self.content_layout.addLayout(self.info_layout)

        # Создаем и добавляем кнопки
        self.save_button = QPushButton("Сохранить в файл")
        self.save_button.setMaximumWidth(180)
        self.save_button.setMinimumHeight(40)
        self.load_button = QPushButton("Загрузить из файла")
        self.load_button.setMaximumWidth(180)
        self.load_button.setMinimumHeight(40)

        self.bottom_buttons_layout = QHBoxLayout()
        self.bottom_buttons_layout.addWidget(self.save_button)
        self.bottom_buttons_layout.addWidget(self.load_button)
        self.content_layout.addLayout(self.bottom_buttons_layout)

        # Подключаем сигналы кнопок
        self.add_car_button.clicked.connect(self.add_passenger)
        self.sort_by_surname_btn.clicked.connect(self.sort_passengers)
        self.save_button.clicked.connect(self.save_to_file)
        self.load_button.clicked.connect(self.load_from_file)

    def draw_passenger_info_layout(self):
        self.passenger_info_layout = QVBoxLayout()
        self.passenger_info_label = QLabel("Ввод данных")
        self.passenger_info_layout.addWidget(self.passenger_info_label)

        self.passenger_info_v_layout = QVBoxLayout()

        # Ввод номера рейса
        self.flight_number_layout = QHBoxLayout()
        self.flight_number_label = QLabel("Номер рейса")
        self.flight_number_input = QSpinBox()
        self.flight_number_input.setMaximumWidth(200)
        self.flight_number_layout.addWidget(self.flight_number_label)
        self.flight_number_layout.addWidget(self.flight_number_input)

        # Ввод даты и времени вылета
        self.departure_datetime_layout = QHBoxLayout()
        self.departure_datetime_label = QLabel("Дата и время вылета")
        self.departure_datetime_input = QDateTimeEdit()
        self.departure_datetime_input.setCalendarPopup(True)
        self.departure_datetime_input.setMaximumWidth(200)
        self.departure_datetime_layout.addWidget(self.departure_datetime_label)
        self.departure_datetime_layout.addWidget(self.departure_datetime_input)

        # Ввод пункта назначения
        self.destination_layout = QHBoxLayout()
        self.destination_label = QLabel("Пункт назначения")
        self.destination_input = QLineEdit()
        self.destination_input.setMaximumWidth(200)
        self.destination_layout.addWidget(self.destination_label)
        self.destination_layout.addWidget(self.destination_input)

        # Ввод фамилии пассажира
        self.passenger_name_layout = QHBoxLayout()
        self.passenger_name_label = QLabel("Фамилия пассажира")
        self.passenger_name_input = QLineEdit()
        self.passenger_name_input.setMaximumWidth(200)
        self.passenger_name_layout.addWidget(self.passenger_name_label)
        self.passenger_name_layout.addWidget(self.passenger_name_input)

        # Ввод количества мест багажа
        self.count_Baggage_layout = QHBoxLayout()
        self.count_Baggage_label = QLabel("Количество мест багажа")
        self.count_Baggage_input = QSpinBox()
        self.count_Baggage_input.setMaximumWidth(200)
        self.count_Baggage_layout.addWidget(self.count_Baggage_label)
        self.count_Baggage_layout.addWidget(self.count_Baggage_input)

        # Ввод веса багажа
        self.weight_Baggage_layout = QHBoxLayout()
        self.weight_Baggage_label = QLabel("Вес багажа")
        self.weight_Baggage_input = QDoubleSpinBox()
        self.weight_Baggage_input.setMaximumWidth(200)
        self.weight_Baggage_layout.addWidget(self.weight_Baggage_label)
        self.weight_Baggage_layout.addWidget(self.weight_Baggage_input)

        # Добавление всех вводов в вертикальный макет
        self.passenger_info_v_layout.addLayout(self.flight_number_layout)
        self.passenger_info_v_layout.addLayout(self.departure_datetime_layout)
        self.passenger_info_v_layout.addLayout(self.destination_layout)
        self.passenger_info_v_layout.addLayout(self.passenger_name_layout)
        self.passenger_info_v_layout.addLayout(self.count_Baggage_layout)
        self.passenger_info_v_layout.addLayout(self.weight_Baggage_layout)

        # Спейсер для улучшения макета
        spacer_top = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.passenger_info_layout.addItem(spacer_top)

        self.passenger_info_layout.addLayout(self.passenger_info_v_layout)

        # Спейсер для улучшения макета
        spacer_bottom = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.passenger_info_layout.addItem(spacer_bottom)

        # Кнопка для добавления багажа
        self.add_car_button = QPushButton("Добавить багаж")
        self.add_car_button.setMinimumWidth(200)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_car_button)
        button_layout.setAlignment(self.add_car_button, Qt.AlignmentFlag.AlignHCenter)
        self.passenger_info_layout.addLayout(button_layout)

    def draw_Baggage_info_layout(self):
        self.search_btn = QPushButton("Искать")
        self.search_layout = QHBoxLayout()

        self.search_input_widget = None

        self.Baggage_info_layout = QVBoxLayout()
        self.Baggage_info_layout.addWidget(QLabel("Данные о багажах"))

        # Комбобокс для фильтров поиска
        self.search_filters_combobox = QComboBox()
        self.search_filters_combobox.addItems(
            [
                "Без фильтра",
                "Номер рейса",
                "Дата вылета",
                "Пункт назначения",
                "Вес багажа",
            ]
        )
        self.search_filters_combobox.currentIndexChanged.connect(self.draw_search_input)
        self.search_layout.addWidget(self.search_filters_combobox)

        self.Baggage_info_layout.addLayout(self.search_layout)
        self.Baggage_info_layout.addWidget(self.search_btn)

        # Список для отображения пассажиров
        self.passengers_list = QListWidget()
        self.Baggage_info_layout.addWidget(self.passengers_list)

        # Кнопка для сортировки пассажиров по фамилии
        self.sort_by_surname_btn = QPushButton("Сортировка по фамилии")
        self.Baggage_info_layout.addWidget(self.sort_by_surname_btn)

    def draw_info_garage_layout(self):
        self.passengers_list.clear()
        for passenger in self.Baggage.passengers:
            item = QListWidgetItem(str(passenger))  # Создаем элемент списка
            self.passengers_list.addItem(item)  # Добавляем элемент в список

    def add_passenger(self):
        flight_number = self.flight_number_input.value()
        departure_datetime = self.departure_datetime_input.dateTime().toString()
        destination = self.destination_input.text()
        passenger_name = self.passenger_name_input.text()
        count_Baggage = self.count_Baggage_input.value()
        weight_Baggage = self.weight_Baggage_input.value()

        # Проверка введенных данных
        if (
            flight_number == 0
            or destination == ""
            or passenger_name == ""
            or count_Baggage == 0
            or weight_Baggage == 0
        ):
            self.show_error_message("Пожалуйста, введите все данные!")
            return

        # Проверка максимального веса багажа для рейса (только если рейс есть в списке)
        try:
            with open("max_weights.json", "r", encoding="UTF-8") as f:
                flights = json.load(f)
                # Ищем рейс в списке
                flight_info = next(
                    (
                        flight
                        for flight in flights
                        if flight["flight_number"] == flight_number
                    ),
                    None,
                )

                # Если рейс найден, проверяем вес
                if flight_info is not None:
                    max_weight = flight_info["max_weight"]
                    # Получаем текущий общий вес багажа для этого рейса
                    current_weight = 0
                    for passenger in self.Baggage.passengers:
                        if passenger.flight_number == flight_number:
                            current_weight += passenger.weight_baggage

                    # Проверяем, не превысит ли новый багаж максимальный вес
                    if current_weight + weight_Baggage > max_weight:
                        self.show_error_message(
                            f"Превышен максимальный вес багажа для рейса {flight_number}!\n"
                            f"Максимальный вес: {max_weight} кг\n"
                            f"Текущий общий вес: {current_weight} кг\n"
                            f"Вес нового багажа: {weight_Baggage} кг\n"
                            f"Доступно для добавления: {max_weight - current_weight} кг"
                        )
                        return
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

        new_passenger = Passenger(
            flight_number=flight_number,
            departure_datetime=departure_datetime,
            destination=destination,
            passenger_name=passenger_name,
            count_baggage=count_Baggage,
            weight_baggage=weight_Baggage,
        )

        if self.Baggage.add_passenger(new_passenger):
            self.draw_info_garage_layout()
            self.clear_inputs()
        else:
            self.show_error_message(
                "Вы не можете добавить еще один багаж, недостаточная вместимость!"
            )

    def sort_passengers(self):
        self.Baggage.sort_by_name()
        self.draw_info_garage_layout()

    def save_to_file(self):
        filename = "Baggage_data.xlsx"
        try:
            self.Baggage.save_to_file(filename)
        except FileNotFoundError:
            self.show_error_message(f"Файла {filename} не найдено, попробуйте еще раз!")
        print("Данные сохранены в файл.")

    def load_from_file(self):
        filename = "Baggage_data.xlsx"
        try:
            self.Baggage.load_from_file(filename)
            self.draw_info_garage_layout()
        except FileNotFoundError as e:
            self.show_error_message(str(e))
        except ValueError as e:
            self.show_error_message(str(e))
        except Exception as e:
            self.draw_info_garage_layout()
            self.show_error_message(str(e))

    def clear_inputs(self):
        self.flight_number_input.clear()
        self.departure_datetime_input.clear()
        self.destination_input.clear()
        self.passenger_name_input.clear()
        self.count_Baggage_input.clear()
        self.weight_Baggage_input.clear()

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def search(self):
        search_filter = self.search_filters_combobox.currentText()
        search_input_text = ""

        # Определение ввода поиска в зависимости от выбранного фильтра
        if search_filter == "Номер рейса":
            search_input_text = str(self.search_input_widget.value())
        elif search_filter == "Дата вылета":
            search_input_text = self.search_input_widget.date().toString("yyyy-MM-dd")
        elif search_filter == "Пункт назначения":
            search_input_text = self.search_input_widget.text()
        elif search_filter == "Вес багажа":
            search_input_text = str(self.search_input_widget.value())
        elif search_filter == "Без фильтра":
            self.draw_info_garage_layout()
            return

        self.passengers_list.clear()

        # Поиск среди пассажиров в зависимости от выбранного фильтра
        for passenger in self.Baggage.passengers:
            if (
                search_filter == "Номер рейса"
                and str(passenger.flight_number) == search_input_text
            ):
                self.passengers_list.addItem(str(passenger))
            elif (
                search_filter == "Дата вылета"
                and passenger.departure_datetime.startswith(search_input_text)
            ):
                self.passengers_list.addItem(str(passenger))
            elif (
                search_filter == "Пункт назначения"
                and search_input_text.lower() in passenger.destination.lower()
            ):
                self.passengers_list.addItem(str(passenger))
            elif (
                search_filter == "Вес багажа"
                and passenger.weight_Baggage == self.search_input_widget.value()
            ):
                self.passengers_list.addItem(str(passenger))

    def draw_search_input(self):
        # Удаление предыдущего виджета ввода поиска, если он существует
        if hasattr(self, "search_input_widget") and self.search_input_widget:
            self.search_layout.removeWidget(self.search_input_widget)
            self.search_input_widget.deleteLater()

        search_filter = self.search_filters_combobox.currentText()
        # Создание соответствующего виджета ввода в зависимости от выбранного фильтра
        if search_filter == "Номер рейса":
            self.search_input_widget = QSpinBox()
        elif search_filter == "Дата вылета":
            self.search_input_widget = QDateEdit()
            self.search_input_widget.setCalendarPopup(True)
        elif search_filter == "Пункт назначения":
            self.search_input_widget = QLineEdit()
        elif search_filter == "Вес багажа":
            self.search_input_widget = QDoubleSpinBox()
        else:
            self.search_input_widget = None

        # Добавление нового виджета ввода поиска в макет
        if self.search_input_widget:
            self.search_layout.insertWidget(0, self.search_input_widget)

        # Подключение кнопки поиска к функции поиска
        self.search_btn.clicked.connect(self.search)
