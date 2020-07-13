from string import ascii_uppercase, punctuation, digits

class Validator:
    def validate(self, value) -> bool:
        return True

class StringSizeValidator(Validator):
    def __init__(self, minimum=0, maximum=20):
        super(StringSizeValidator, self).__init__()
        self.minimum = minimum
        self.maximum = maximum

    def validate(self, value):
        return len(value) >= self.minimum and len(value) <= self.maximum

class EmailValidator(StringSizeValidator):
    def __init__(self):
        super(EmailValidator, self).__init__(minimum=8, maximum=100)

    def validate(self, value):
        return ("@" in value) and ("." in value) and super(EmailValidator, self).validate(value)

class PasswordValidator(StringSizeValidator):
    def __init__(self, minimum=8, minupper=1, minnumber=1, minspecial=1):
        super(PasswordValidator, self).__init__(maximum=200, minimum=minimum)
        self.minupper = minupper
        self.minnumber = minnumber
        self.minspecial = minspecial

    def validate(self, value):
        upper = 0
        number = 0
        special = 0

        for char in value:
            upper += 1 if char in ascii_uppercase else 0
            number += 1 if char in digits else 0
            special += 1 if char in punctuation else 0

        return (upper >= self.minupper) and (number >= self.minnumber) and (special >= self.minspecial) and super(PasswordValidator, self).validate(value)

class RangeValidator(Validator):
    def __init__(self, from_=0, to=100):
        super(RangeValidator, self).__init__()
        self.from_ = from_
        self.to = to

    def validate(self, value):
        return value in range(self.from_, self.to+1)