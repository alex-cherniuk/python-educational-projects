import numpy as np
from datetime import datetime


class TicketOrder:
    def __init__(self, current_date):
        self.tickets_dict = {}
        self.current_date = current_date

    def add_ticket(self, event, student):
        ticket = Ticket(event, self.current_date, student)
        if ticket in self.tickets_dict.keys():
            self.tickets_dict[ticket] += 1
        self.tickets_dict[ticket] = 1

    @property
    def total_cost(self):
        return sum([ticket.price * self.tickets_dict[ticket] for ticket in self.tickets_dict.keys()])

    def reset(self):
        self.tickets_dict = {}

    def __str__(self):
        printable_order_list = []
        for ticket in self.tickets_dict.keys():
            printable_order_list.append(f"{self.tickets_dict[ticket]}\t{ticket}")
        return '*' * 120 + '\nTicket in order:\n' + '\n'.join(
            printable_order_list) + f'\nTotal cost: {self.total_cost}\n' + '*' * 120


class Event:
    def __init__(self, title, date, regular_price_ticket):
        self.title = title
        self.date = date
        self.regular_price_ticket = regular_price_ticket
        self.tickets_ordered = 0

    def __str__(self):
        return "{}\t{}\tPrice: {}".format(self.date.strftime('%Y-%m-%d'), self.title, self.regular_price_ticket)


class Ticket:
    def __init__(self, event, current_date, student=False):
        self.event = event
        self.event.tickets_ordered += 1
        self.student = student
        self.current_date = current_date

    @property
    def discount(self):
        if self.student:
            return 50
        day_purchased = self.event.date - self.current_date
        if day_purchased.days >= 60:
            return 40
        elif day_purchased.days >= 10:
            return 10
        return 0

    @property
    def identifier(self):
        return hash(self.event.title + self.event.date.strftime('%Y%m%d') +
                    self.current_date.strftime('%Y%m%d') + str(self.event.tickets_ordered))

    @property
    def price(self):
        return (1 - self.discount / 100) * self.event.regular_price_ticket

    def __eq__(self, other):
        if isinstance(other, Ticket):
            return self.event.title == other.event.title and self.event.date == other.event.date
        raise NotImplemented

    def __hash__(self):
        return self.identifier

    def __str__(self):
        return "{} ID{} {}".format(self.event.date.strftime('%Y/%m/%d'), self.identifier, self.event.title)


class Client:
    def __init__(self, name, phone=None, student=False):
        self.name = name
        self.phone = phone
        self.student = student

    def __str__(self):
        return f"I am {self.name}"

    def order_ticket(self, event, order):
        order.add_ticket(event, self.student)
        return order


def generate_random_date(year=2019):
    month = np.random.randint(1, 12)
    day = np.random.randint(1, 28)
    return datetime(year, month, day)


def generate_list_unique_dates(current_date, number):
    dates = []
    while len(dates) < number:
        date = generate_random_date()
        if date < current_date:
            continue
        dates.append(date)
        if len(set(dates)) == len(dates):
            dates = list(set(dates))
            continue
    return dates


event_titles = ["Data Science UA Conference",
                "Data Sciense Competition",
                "Vodafone Data Science Insights",
                "AISaturdays in Innovecs",
                "AISaturdays in Sigma Software University"]


def generate_future_events(current_date, number_of_events):
    dates = generate_list_unique_dates(current_date, number_of_events)
    titles = np.random.choice(event_titles, number_of_events)
    event_cost = np.random.randint(100, 1000, 5)
    events_list = []
    for title, date, cost in zip(titles, dates, event_cost):
        events_list.append(Event(title, date, cost))
    return events_list


if __name__ == "__main__":

    current_day = generate_random_date()
    print(f"Today is {current_day.strftime('%Y/%m/%d')}")

    events = generate_future_events(current_day, 5)
    new_client = Client("Vasya", 555555)
    print(new_client)

    new_order = TicketOrder(current_day)
    new_client.order_ticket(np.random.choice(events), new_order)
    print(new_order)
