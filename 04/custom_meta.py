class CustomMeta(type):
    '''
    к существующим атрибутам можно обращаться только через custom_
    при создании нового атрибута custom_ не указывается
    '''

    @classmethod
    def __prepare__(mcs, name, bases): # pylint: disable=unused-argument
        def __getattribute__(self, item):
            if len(item) >= 4 and item[:2] == item[-2:] == '__':
                return object.__getattribute__(self, item)
            if item[:7] == 'custom_':
                return object.__getattribute__(self, item[7:])
            raise AttributeError(f'{item} not starts with custom_')

        def __setattr__(self, key, value):
            if key[:7] == 'custom_':
                if key[7:] in self.__dict__:
                    object.__setattr__(self, key[7:], value)
                else:
                    raise AttributeError(f'{key} not found')
            else:
                if key in self.__dict__:
                    raise AttributeError(f'{key} not starts with custom_')
                object.__setattr__(self, key, value)

        return {'__getattribute__': __getattribute__,
                '__setattr__': __setattr__}

    def __getattribute__(cls, item):
        if len(item) >= 4 and item[:2] == item[-2:] == '__':
            return super().__getattribute__(item)
        if item[:7] == 'custom_':
            return super().__getattribute__(item[7:])
        raise AttributeError(f'{item}  not starts with custom_')

    def __setattr__(cls, key, value):
        if key[:7] == 'custom_':
            if key[7:] in cls.__dict__:
                super().__setattr__(key[7:], value)
            else:
                raise AttributeError(f'{key} not found')
        else:
            if key in cls.__dict__:
                raise AttributeError(f'{key} not starts with custom_')
            super().__setattr__(key, value)
