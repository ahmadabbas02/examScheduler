import time


class Course:
    def __init__(self, name, date, time):
        self.name = name
        self.date = date
        self.time = time

    def __repr__(self):
        date_string = time.strftime("%d/%m/%Y", self.date)
        time_string = time.strftime("%H:%M", self.time)
        return '{' + self.name + ', ' + date_string + ', ' + time_string + '}'
