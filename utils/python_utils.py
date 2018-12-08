class CannotHandled(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class CannotRemove(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def split_into(arr, n):
    sp = len(arr) // n
    if sp == 0:
        return [[x, ] for x in arr]
    return [arr[i:i + sp] for i in range(0, len(arr), sp)]


class create_worker:
    def __init__(self, target):
        self.target = target

    def __call__(self, args):
        r = []
        for idx, arg in enumerate(args):
            r.append(self.target(arg))
        return r
