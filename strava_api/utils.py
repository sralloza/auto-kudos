"""Utils module."""


# Downloaded from https://github.com/sralloza/vcm/blob/master/vcm/core/utils.py#L432
class MetaSingleton(type):
    """Metaclass to always make class return the same instance."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
