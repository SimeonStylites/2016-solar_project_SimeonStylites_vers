# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

space_width = 600
"""Ширина области моделирования"""

space_height = 600
"""Высота области моделирования"""

graphics_width = 400
"""Ширина графиков"""

scale_factor = None
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""

array_vt = []
v_max = 1
"""данные для графика v от t"""


def calculate_scale_factor(max_distance):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global scale_factor
    scale_factor = 0.4 * min(space_height, space_width) / max_distance
    print('Scale factor:', scale_factor)


def scale_x(x):
    """Возвращает экранную **x** координату по **x** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **x** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.

    Параметры:

    **x** — x-координата модели.
    """

    return int(x*scale_factor) + space_width//2


def scale_y(y):
    """Возвращает экранную **y** координату по **y** координате модели.
    Принимает вещественное число, возвращает целое число.
    В случае выхода **y** координаты за пределы экрана возвращает
    координату, лежащую за пределами холста.
    Направление оси развёрнуто, чтобы у модели ось **y** смотрела вверх.

    Параметры:

    **y** — y-координата модели.
    """

    return -int(y*scale_factor) + space_height//2


def create_star_image(space, star):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """

    x = scale_x(star.x)
    y = scale_y(star.y)
    r = star.R
    star.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=star.color)


def create_planet_image(space, planet):
    """Создаёт отображаемый объект планеты.

    Параметры:

    **space** — холст для рисования.
    **planet** — объект планеты.
    """

    x = scale_x(planet.x)
    y = scale_y(planet.y)
    r = planet.R
    planet.image = space.create_oval([x - r, y - r], [x + r, y + r], fill=planet.color)


def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    space.create_text(30, 80, tag="header", text=system_name, font=header_font)


def update_object_position(space, body):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    x = scale_x(body.x)
    y = scale_y(body.y)
    r = body.R
    if x + r < 0 or x - r > space_width or y + r < 0 or y - r > space_height:
        space.coords(body.image, space_width + r, space_height + r,
                     space_width + 2 * r, space_height + 2 * r)  # положить за пределы окна
    space.coords(body.image, x - r, y - r, x + r, y + r)


def plot_graph_vt(graphic_space, objects, planet_number, time, timestep):
    global v_max
    # оси графика v от t
    graphic_space.create_line(0, space_height / 3 - 5, graphics_width, space_height / 3 - 5, width=2, fill="white")
    graphic_space.create_line(5, 0, 5, space_height / 3, width=2, fill='white')
    # график v от t
    v_max = 3*objects[planet_number].Vinit
    x = 5 + time/timestep
    y = (space_height / 3 - 5) * (1 - objects[planet_number].v_abs() / v_max)
    graphic_space.create_line(x, y, x + 1, y + 1, fill='white')

def plot_graph_rt(graphic_space, objects, planet_number, time, timestep):
    global r_max
    # оси графика r от t
    graphic_space.create_line(0, space_height*2 / 3 - 5, graphics_width, space_height*2 / 3 - 5, width=2, fill="white")
    graphic_space.create_line(5, space_height / 3, 5, space_height*2 / 3, width=2, fill='white')
    # график r от t
    r_max = 3*((objects[0].xinit-objects[planet_number].xinit)**2+(objects[0].yinit-objects[planet_number].yinit)**2)**0.5
    x = 5 + time/timestep
    y = (space_height / 3 - 5) * (2 - objects[planet_number].r_to_star(objects[0]) / r_max)+5
    graphic_space.create_line(x, y, x + 1, y + 1, fill='white')


def plot_graph_vr(graphic_space, objects, planet_number):
    # оси графика v от r
    graphic_space.create_line(0, space_height - 5, graphics_width, space_height - 5, width=2, fill="white")
    graphic_space.create_line(5, space_height*2 / 3, 5, space_height, width=2, fill='white')
    # график v от r
    x = 5 + (graphics_width - 5) * objects[planet_number].r_to_star(objects[0]) / r_max
    y = (space_height / 3 - 5) * (3 - objects[planet_number].v_abs() / v_max)+10
    graphic_space.create_line(x, y, x + 1, y + 1, fill='white')


def clear_graphs(graphic_vt):
    graphic_vt.create_rectangle(0, 0, graphics_width, space_height, fill='black')


if __name__ == "__main__":
    print("This module is not for direct call!")
