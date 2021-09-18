from math import *

def square(num):
    return num**2

def calc(Xpos, Ypos, Zpos, Qpos, L0, L1, L2, L2r, L2pr, L3, Lsrv):
    Xp = Xpos
    Yp = Ypos
    Zp = Zpos - L0  # скорректированная координата Z  mm
    Qp = Qpos

    a0 = round(atan2(Yp, Xp)*57.3)  # Угол поворота 0-й оси относительно выбранного вами 0 ° начала координат в плоскости XY
    # В резульате этого поворота попадаем в основную рабочую плоскость
    # Основная плоскость - в которой происходит движение звеньев L1, L2, L3.
    Xt = round(sqrt(square(Xp) + square(Yp)))   # Координата X целевой  точки в основной плоскости движения звеньев L1, L2 и L3

    dX = round(L3*sin(Qp/57.3))  # Корректировка X на ориентацию 3-го звена (L3)
    dY = round(L3*cos(Qp/57.3))  # Корректировка Y на ориентацию 3-го звена (L3)

    Xn = Xt - dX    # Позиция X в основной плоскости, куда должен попасть шарнир 3-го звена
    Yn = Zp + dY    # Позиция Y в основной плоскости, куда должен попасть шарнир 3-го звена

    d = round(sqrt(square(Xn) + square(Yn)))    # Длина отрезка между 1-м и 3-м  шарнирами
    q1 = atan2(Yn, Xn) * 57.3  # Вспомогательный угол 1

    sq2 = (square(d) + square(L1) - square(L2)) / (L1 * d * 2)
    q2 = acos(sq2)*57.3

    sq3 = (square(L1) + square(L2) - square(d)) / (L1 * L2 * 2)
    q3 = acos(sq3)*57.3

    a1 = 180 - round(q1 + q2)   # Угол поворота сервомотора 1-й оси относительно горизонтали. 0° - сзади!!!
    a2t = 180 - round(q3)   # Угол поворота сервомотора 2-й оси относительно 1-й
    a3 = 200 - round(q2 + q3 + q1) + Qp  # Угол поворота сервы 3, где 0°  отклонен на 70° снизу от L2
    a4 = 90  # Угол поворота захвата

    Lac = round(sqrt(square(L1) + square(L2r) - 2 * L1 * L2r * cos(a2t/57.3)))
    cAb = acos((square(L1) + square(Lac) - square(L2r)) / (2 * L1 * Lac))*57.3

    eAc = a1 - cAb
    Lce = round(sqrt(square(Lsrv) + square(Lac) - 2 * Lsrv * Lac * cos(eAc/57.3)))

    cEa = acos((square(Lce) + square(Lsrv) - square(Lac)) / (2 * Lce * Lsrv)) * 57.3
    dEc = acos((square(Lce) + square(L2pr) - square(L1)) / (2 * Lce * L2pr)) * 57.3

    a2 = round(210 - dEc - cEa)  # Угол поворота сервы 2 относительно горизонтали - 30°
