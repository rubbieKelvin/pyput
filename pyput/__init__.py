from . import validators

def _typed_list(container):
    res = []

    for item in container:
        if type(item) in [int, str, bool]:
            res.append(type(item))
        elif type(item) == list:
            res.append(_typed_list(item))
        elif type(item) == dict:
            res.append(_typed_dict(item))
    return res
    
def _typed_dict(container):
    res = {}

    for key in container:
        if type(container[key]) in [int, str, bool]:
            res[key] = type(container[key])
        elif type(container[key]) == list:
            res[key] = _typed_list(container[key])
        elif type(container[key]) == dict:
            res[key] = _typed_dict(container[key])
    return res

def typed(container):
    if type(container) == list:
        return _typed_list(container)
    else:
        return _typed_dict(container)

def is_function(value) -> bool:
    def _(): pass
    return (type(value) == type(_)) or (type(value) == type(lambda _: None)) 


class CliInput:
    def __init__(self, prompt="", validator=lambda x: True):
        self.prompt = prompt
        self.validate = validator
        
    def __validate(self, value) -> bool:
        if type(self.validate) == bool:
            return bool
        if is_function(self.validate):
            return self.validate(value)

        if hasattr(self.validate, "validate"):
            self.validate:validators.Validator  # annotation
            return self.validate.validate(value)
        
        return False

    def _validate(self, value) -> bool:
        if type(self.validate) == dict:
            validator = dict(int=True, str=True)
            validator.update(self.validate)
            return validator[type(int)](value)
        return self.__validate(value)

    def _int(self):
        while True:
            res = input(self.prompt)
            if res.isdigit():
                res = int(res)
                if self._validate(res):
                    return res

    def _bool(self):
        return bool(input(self.prompt))

    def _str(self):
        while True:
            res = input(self.prompt)
            if self._validate(res):
                return res

    def _list(self, types):
        res = [None for _ in types]
        prevprompt = self.prompt

        for index, typ in enumerate(types):
            self.prompt = prevprompt+f"[{index}]"
            if typ == int:
                res[index] = self._int()
            elif typ == str:
                res[index] = self._str()
            elif typ == bool:
                res[index] = self._bool()
            elif type(typ) == list:
                res[index] = self._list(typ)
            elif type(typ) == dict:
                res[index] = self._dict(typ)
            self.prompt = prevprompt
        return res

    def _dict(self, mapping):
        result = dict()
        prevprompt = self.prompt

        for key in mapping:
            self.prompt = prevprompt+f"[{key}]"

            if mapping[key] == int:
                result[key] = self._int()
            elif mapping[key] == str:
                result[key] = self._str()
            elif mapping[key] == bool:
                result[key] = self._bool()
            elif type(mapping[key]) == list:
                result[key] = self._list(mapping[key])
            elif type(mapping[key]) == dict:
                result[key] = self._dict(mapping[key])
            self.prompt = prevprompt
        return result

    def result(self, *args, **kwargs):
        if not args and not kwargs: raise TypeError("no type specified!")

        if len(args) == 1:
            typ = args[0]

# -> STRING
            if typ == str:
                res = self._str()

# -> BOOLEAN
            elif typ == bool:
                res = self._bool()

# -> INTEGER
            elif typ == int:
                res = self._int()

# -> LIST [1]
            elif type(typ) == list:
                res = self._list(typ)

# -> DICT [1]
            elif type(typ) == dict:
                res = self._dict(typ)

        elif args and not kwargs:
# -> LIST
            res = self._list(args)

        elif not args and kwargs:
# -> DICT
            res = self._dict(kwargs)
        return res
