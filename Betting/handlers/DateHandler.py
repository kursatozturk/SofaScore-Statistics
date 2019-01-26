import arrow
class DateHandler:
    # A very meaningless implementation
    # will be removed in free time
    TODAY = None

    def __init__(self, dt):
        self.__dm = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.year, self.month, self.day = [int(x) for x in dt.split('-')]
        if self.leap_year():
            self.__dm[2] = 29

    def leap_year(self):
        return not self.year % 4

    def __parse_it(self):
        s = "{0:0004d}-{1:02d}-{2:02d}"
        return s.format(self.year, self.month, self.day)

    def incr(self):
        self.day += 1
        if self.day > self.__dm[self.month]:
            self.day = 1
            self.month += 1
            if self.month == 13:
                self.month = 1
                self.year += 1
                if self.leap_year():
                    self.__dm[2] = 29
                else:
                    self.__dm[2] = 28

    def create_interval_till(self, end_date=None):
        if not end_date:
            end_date = arrow.now().format("YYYY-MM-DD")

        traverser = DateHandler(str(self))  # create a copy

        end_date = DateHandler(end_date)
        end_date.incr()
        interval = list()
        while traverser != end_date:
            interval.append(str(traverser))
            traverser.incr()
        return interval

    def __str__(self):
        return self.__parse_it()

    def __eq__(self, rhs):
        if type(rhs) is str:
            rhs = DateHandler(rhs)
        return self.year == rhs.year and self.month == rhs.month and self.day == rhs.day

    def __lt__(self, rhs):
        if type(rhs) is str:
            rhs = DateHandler(rhs)
        if self.year == rhs.year:
            if self.month == rhs.month:
                return self.day < rhs.day
            return self.month < rhs.month
        return self.year < rhs.year

    def __gt__(self, rhs):
        return rhs < self

    def __le__(self, rhs):
        return self < rhs or self == rhs

    def __ge__(self, rhs):
        return rhs < self or self == rhs

    def __ne__(self, rhs):
        return not self == rhs
