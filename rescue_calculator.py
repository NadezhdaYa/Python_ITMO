import math

def convert_yards_to_feet(yards: float) -> float:
    """Конвертирует ярды в футы (1 ярд = 3 фута)."""
    return yards * 3.0

def convert_mph_to_fps(miles_per_hour: float) -> float:
    """
    Конвертирует мили в час в футы в секунду.
    1 миля = 5280 футов, 1 час = 3600 секунд.
    """
    feet_per_hour = miles_per_hour * 5280.0
    return feet_per_hour / 3600.0

def calculate_time_for_angle(
    d1_yards: float,
    d2_feet: float,
    h_yards: float,
    v_sand_mph: float,
    n: float,
    theta1_degrees: float
) -> float:
    """
    Рассчитывает время достижения утопающего для конкретного угла theta1.
    Возвращает только время (в секундах).

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
    v_sand_fps = convert_mph_to_fps(v_sand_mph)
    v_water_fps = v_sand_fps / n

    # Угол в радианах
    theta1_radians = math.radians(theta1_degrees)

    # Горизонтальное расстояние по песку до точки входа в воду
    x = d1_feet * math.tan(theta1_radians)

    # Расстояния D1 (по песку) и D2 (вплавь)
    D1 = math.sqrt(d1_feet ** 2 + x ** 2)
    D2 = math.sqrt((h_feet - x) ** 2 + d2_feet ** 2)

    # Общее время: время по песку + время в воде
    time_seconds = (D1 / v_sand_fps) + (D2 / v_water_fps)
    return time_seconds