from math import floor


class JWTAge:
    def __init__(self, birth: float):
        self.secs = round(birth)
        self.minutes = floor(self.secs / 60)
        self.secs -= self.minutes * 60
        self.hours = floor(self.minutes / 60)
        self.minutes -= self.hours * 60

    def __str__(self):
        return f"age='{self.hours}h {self.minutes}min {self.secs}sec'"
