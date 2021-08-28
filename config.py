
class cfg:
    CONNECT_TO_MAIN = False
    CONNECT_TO_HAND = False

    IP_MAIN = "192.168.137.246"
    IP_HAND = "192.168.137.18"

    PORT = 23

    CSV_PATH = "points_new.csv"

    WIDTH = 1200
    HEIGHT = 350  # настройки
    FPS = 60

    TITLE = "Bilinear interpolation"

    LENS = {
        "shoulder": 250,
        "wrist": 240,
        "hand": 100
    }

    HAND_MAX_X = 290
    HAND_MIN_X = 150
    HAND_MAX_Y = 290
    HAND_MIN_Y = -270