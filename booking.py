from datetime import datetime
import random

ALPH = 'abcdefghijklmnopqrstuvwxyz'
SEP_LEN = 30


class BookingError(Exception):
    pass


class ServiceLevel:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Airport:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Flight:
    def __init__(self, departure: Airport, arrival: Airport, date: datetime, flight_number: str):
        self.departure = departure
        self.arrival = arrival
        self.date = date
        self.flight_number = flight_number
        self.seating_configuration: list[tuple[ServiceLevel, str]] = []
        self.total_seats = 0
        self.booked_seats = set()

    def add_seats(self, service_level: ServiceLevel, rows_count: int, row_scheme: str):  # шаблон "ххх ххх"
        for _ in range(rows_count):
            self.seating_configuration.append((service_level, row_scheme))
            self.total_seats += row_scheme.count("x")

    def check_seat(self, row_num: int, seat_num: str):
        if row_num > len(self.seating_configuration) or row_num <= 0:
            raise BookingError("Указанный ряд не существует")
        seat_idx = ALPH.find(seat_num.lower())
        if seat_idx < 0 or seat_idx >= self.seating_configuration[row_num - 1][1].count("x"):
            raise BookingError("Указанное место не существует")

    def book_seat(self, row_num: int, seat_num: str):
        self.check_seat(row_num, seat_num)
        if (row_num, seat_num) in self.booked_seats:
            raise BookingError("Место уже занято")
        self.booked_seats.add((row_num, seat_num))

    def book_cancel(self, row_num: int, seat_num: str):
        self.check_seat(row_num, seat_num)
        if (row_num, seat_num) not in self.booked_seats:
            raise BookingError("Место не забронировано")
        self.booked_seats.remove((row_num, seat_num))

    def get_configuration(self):
        res = ["ПЛАН МЕСТ", "-" * SEP_LEN]
        cur_sl = None
        for i, (sl, scheme) in enumerate(self.seating_configuration):
            if sl != cur_sl:
                res.append(str(sl))
                cur_sl = sl
                line = "   "
                seat_idx = 0
                for t in scheme:
                    if t == " ":
                        t = "   "
                    else:
                        t = f" {ALPH[seat_idx]} "
                        seat_idx += 1
                    line += t
                res.append(line)
            line = str(i + 1).rjust(2, ' ') + " "
            u = 0
            for s, c in enumerate(scheme):
                if c == " ":
                    c = "   "
                    u += 1
                else:
                    c = f"[{'x' if (i + 1, ALPH[s - u]) in self.booked_seats else ' '}]"
                line += c
            res.append(line)

        res.append("-" * SEP_LEN)

        return "\n".join(res)

    def __str__(self):
        return f"{self.flight_number} {self.date:%d.%m.%Y %H:%M} {self.departure} -> {self.arrival}"

    def check_free(self, count: int):
        return self.total_seats - len(self.booked_seats) >= count


a1 = Airport("Толмочёво")
a2 = Airport("Домодедово")
business = ServiceLevel("Бизнес класс")
economy = ServiceLevel("Эконом класс")
flight = Flight(a1, a2, datetime.now(), "S1310")
flight.add_seats(business, 2, "xx xx")
flight.add_seats(economy, 10, "xxx xxx")
flight.book_seat(12,"f")
flight.book_seat(5,"a")
flight.book_seat(5,"b")
flight.book_seat(5,"c")
flight.book_seat(7,"d")
flight.book_seat(7,"f")
flight.book_seat(4,"b")
flight.book_seat(3,"a")
flight.book_seat(4,"a")
flight.book_seat(1,"d")
flight.book_seat(2,"b")
flight.book_seat(10,"e")
flight.book_seat(10,"f")
