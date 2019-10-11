class Transaction:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        for k, v in kwargs.items():
            if isinstance(v, dict):
                self.__dict__[k] = Transaction(**v)