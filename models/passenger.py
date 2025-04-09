class Passenger:
    def __init__(self, flight_number, departure_datetime, destination, passenger_name, count_baggage, weight_baggage):
        self.flight_number = flight_number
        self.departure_datetime = departure_datetime
        self.destination = destination
        self.passenger_name = passenger_name
        self.count_baggage = count_baggage
        self.weight_baggage = weight_baggage



    def __str__(self):
        return f"\nНомер рейса: {self.flight_number}\nДата и время вылета: {self.departure_datetime}\nПункт назначения: {self.destination}\nФамилия пассажира: {self.passenger_name}\nКоличество мест багажа: {self.count_baggage}\nСуммарный вес багажа: {self.weight_baggage}\n"
