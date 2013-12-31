class Colours(dict):
    def __init__(self, *args, **kwargs):
        super(Colours, self).__init__(*args, **kwargs)
        self.__dict__ = self


colours = Colours({
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (230, 230, 44),
    "dark_green": (0, 155, 0),
    "dark_grey": (40, 40, 40),
    "light_grey": (235, 235, 235),
})
