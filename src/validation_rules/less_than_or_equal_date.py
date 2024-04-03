class LessThanOrEqualDate:
    def __init__(self, date):
        self.date = date
        self.error_message = 'Date must be less than %s' % date

    def validate(self, value) -> bool:
        return value <= self.date
