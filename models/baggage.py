import openpyxl
from models.passenger import Passenger


class Baggage:
    def __init__(self):
        self.passengers = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        return True

    def save_to_file(self, filename):
        try:
            try:
                wb = openpyxl.load_workbook(filename)
                ws = wb.active
            except FileNotFoundError:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Информация о багажах пассажиров"
                headers = [
                    "Номер рейса",
                    "Дата и время вылета",
                    "Пункт назначения",
                    "Фамилия пассажира",
                    "Количество мест багажа",
                    "Суммарный вес багажа",
                ]
                ws.append(headers)

            for passenger in self.passengers:
                ws.append(
                    [
                        passenger.flight_number,
                        passenger.departure_datetime,
                        passenger.destination,
                        passenger.passenger_name,
                        passenger.count_bagage,
                        passenger.weight_bagage,
                    ]
                )

            wb.save(filename)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")
            return False

    def load_from_file(self, filename):
        try:
            wb = openpyxl.load_workbook(filename)
            ws = wb.active

            records_found = False
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row and len(row) >= 6 and all(cell is not None for cell in row):
                    records_found = True
                    flight_number, departure_datetime, destination, passenger_name, count_bagage, weight_bagage = row
                    passenger = Passenger(flight_number, departure_datetime, destination, passenger_name, count_bagage, weight_bagage)
                    self.add_passenger(passenger)

            if not records_found:
                raise ValueError(f"В файле {filename} нет записей!")

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден.")

    def sort_by_name(self):
        self.passengers.sort(key=lambda passenger: passenger.passenger_name)
