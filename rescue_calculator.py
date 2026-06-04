import math

def convert_yards_to_feet(yards):
    """Конвертирует ярды в футы (1 ярд = 3 фута)."""
    return yards * 3

def convert_miles_per_hour_to_feet_per_second(miles_per_hour):
    """
    Конвертирует мили в час в футы в секунду.
    1 миля = 5280 футов, 1 час = 3600 секунд.
    """
    feet_per_hour = miles_per_hour * 5280
    return feet_per_hour / 3600

def calculate_rescue_time(d1_yards, d2_feet, h_yards, v_sand_mph, n, theta1_degrees):
    """
    Рассчитывает общее время, необходимое спасателю для достижения утопающего.

    Параметры:
    - d1_yards: расстояние от спасателя до кромки воды (ярды)
    - d2_feet: расстояние от утопающего до берега (футы)
    - h_yards: боковое смещение между спасателем и утопающим (ярды)
    - v_sand_mph: скорость движения по песку (мили в час)
    - n: коэффициент замедления в воде
    - theta1_degrees: направление движения по песку (градусы)

    Возвращает:
    - time_seconds: общее время в секундах (float)
    - theta1_int: угол в градусах как целое число (int)
    """

    # Конвертируем все расстояния в футы
    d1_feet = convert_yards_to_feet(d1_yards)
    h_feet = convert_yards_to_feet(h_yards)

    # Конвертируем скорость из миль/час в футы/секунду
    v_sand_fps = convert_miles_per_hour_to_feet_per_second(v_sand_mph)

    # Скорость в воде (меньше из‑за коэффициента замедления)
    v_water_fps = v_sand_fps / n

    # Конвертируем угол из градусов в радианы для тригонометрических функций
    theta1_radians = math.radians(theta1_degrees)

    # Рассчитываем x — горизонтальное расстояние по песку до точки входа в воду
    x = d1_feet * math.tan(theta1_radians)

    # Рассчитываем D1 — расстояние по песку
    D1 = math.sqrt(d1_feet ** 2 + x ** 2)

    # Рассчитываем D2 — расстояние вплавь
    D2 = math.sqrt((h_feet - x) ** 2 + d2_feet ** 2)

    # Общее время: время по песку + время в воде
    time_seconds = (D1 / v_sand_fps) + (D2 / v_water_fps)

    # Округление угла до целого числа
    theta1_int = int(round(theta1_degrees))

    return time_seconds, theta1_int