from rescue_calculator import (
    convert_yards_to_feet,
    convert_mph_to_fps,
    calculate_time_for_angle,
)
import math

# МОДУЛЬНЫЕ ТЕСТЫ

def run_unit_tests():
    """Запускает набор модульных тестов для функций из rescue_calculator."""
    print("\n=== Запуск модульных тестов ===\n")

    # Тест 1: конвертация ярдов в футы
    assert abs(convert_yards_to_feet(1.0) - 3.0) < 1e-9, "Тест 1 не пройден"
    assert abs(convert_yards_to_feet(8.0) - 24.0) < 1e-9, "Тест 1 не пройден"
    print("✅ Тест 1 пройден: конвертация ярдов → футы")

    # Тест 2: конвертация миль/час → футы/секунду
    # 1 mph = 5280 / 3600 fps ≈ 1.466666...
    expected_fps_1mph = 5280.0 / 3600.0
    assert abs(convert_mph_to_fps(1.0) - expected_fps_1mph) < 1e-9, "Тест 2 не пройден"
    assert abs(convert_mph_to_fps(5.0) - 5.0 * expected_fps_1mph) < 1e-9, "Тест 2 не пройден"
    print("✅ Тест 2 пройден: конвертация mph → fps")

    # Тест 3: расчёт времени
    t1 = calculate_time_for_angle(8.0, 10.0, 50.0, 5.0, 2.0, 30.0)
    t2 = calculate_time_for_angle(8.0, 10.0, 50.0, 5.0, 2.0, 45.0)
    assert t1 > 0 and t2 > 0, "Тест 3 не пройден: время должно быть положительным"
    print(f"✅ Тест 3 пройден: t(30°)={t1:.2f}, t(45°)={t2:.2f}")

    print("\n=== Все модульные тесты пройдены ===\n")

# Запускаем тесты сразу при импорте/запуске скрипта
run_unit_tests()

# ВВОД/ВЫВОД

def get_float_input(prompt: str) -> float:
    """Безопасный ввод вещественного числа с подсказкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите корректное число.")

def find_optimal_angle_by_loop(
    d1_yards: float,
    d2_feet: float,
    h_yards: float,
    v_sand_mph: float,
    n: float,
    angle_start: float = 0.0,
    angle_end: float = 90.0,
    step: float = 0.1
) -> tuple[float, float]:
    """
        Перебирает углы от angle_start до angle_end с шагом step,
        находит угол, при котором время минимально.
        Возвращает: (optimal_theta_degrees, min_time_seconds)
    """

    min_time = float('inf')
    optimal_theta = angle_start

    current_angle = angle_start
    while current_angle <= angle_end:
        # Защита от выхода за пределы области определения tan (близко к 90°)
        if abs(current_angle - 90.0) < 1e-6:
            current_angle += step
            continue

        time_sec = calculate_time_for_angle(
            d1_yards, d2_feet, h_yards, v_sand_mph, n, current_angle
        )
        if time_sec < min_time:
            min_time = time_sec
            optimal_theta = current_angle

        current_angle += step

    return optimal_theta, min_time

def main():
    """Основная функция программы — запрашивает данные у пользователя и выводит результат."""
    print("Расчёт времени спасения утопающего и подбор оптимального угла")
    print("=" * 60)

    d1 = get_float_input("Введите расстояние между спасателем и кромкой воды, d1 (ярды) => ")
    d2 = get_float_input("Введите расстояние от утопающего до берега, d2 (футы) => ")
    h = get_float_input("Введите боковое смещение между спасателем и утопающим, h (ярды) => ")
    v_sand = get_float_input("Введите скорость движения спасателя по песку, v_sand (мили в час) => ")
    n = get_float_input("Введите коэффициент замедления спасателя при движении в воде, n => ")

    # Подбор оптимального угла численно
    opt_theta, opt_time = find_optimal_angle_by_loop(d1, d2, h, v_sand, n)

    print("\n--- Результаты численного подбора (цикл) ---")
    print(f"Оптимальный угол: {opt_theta:.2f}°")
    print(f"Минимальное время: {opt_time:.2f} сек")

    # Аналитическое решение (см. пояснение ниже)
    analytical_theta = compute_snell_angle(d1, d2, h, v_sand, n)
    analytical_time = calculate_time_for_angle(d1, d2, h, v_sand, n, analytical_theta)

    print("\n--- Аналитическое решение (закон Снеллиуса) ---")
    print(f"Угол (аналитически): {analytical_theta:.2f}°")
    print(f"Время (аналитически): {analytical_time:.2f} сек")

    print("\n--- Сравнение ---")
    diff_angle = abs(opt_theta - analytical_theta)
    diff_time = abs(opt_time - analytical_time)
    print(f"Разница углов: {diff_angle:.4f}°")
    print(f"Разница времени: {diff_time:.4f} сек")


def compute_snell_angle(
        d1_yards: float,
        d2_feet: float,
        h_yards: float,
        v_sand_mph: float,
        n: float
) -> float:
    """
    Аналитическое решение через закон Снеллиуса (принцип наименьшего времени).

    Обозначения:
      d1 — перпендикуляр от спасателя до берега (в футах)
      d2 — перпендикуляр от утопающего до берега (в футах)
      h — общее боковое смещение (в футах)
      v1 = v_sand — скорость на суше
      v2 = v_sand / n — скорость в воде

    Закон Снеллиуса для задачи о спасателе:
      sin(theta1) / v1 = sin(theta2) / v2

    Геометрически:
      x — точка входа в воду (отсчитывается от проекции спасателя)
      theta1 = atan(x / d1)
      theta2 = atan((h - x) / d2)

    Уравнение:
      (x / sqrt(x^2 + d1^2)) / v1 = ((h - x) / sqrt((h - x)^2 + d2^2)) / v2

    Можно выразить угол theta1 напрямую из условия:
      sin(theta1) = (v1 / v2) * sin(theta2),
    но проще численно решить уравнение относительно x, а затем найти theta1.

    Реализуем численное решение уравнения Снеллиуса методом бисекции.
    """

    import math

    d1_ft = convert_yards_to_feet(d1_yards)
    h_ft = convert_yards_to_feet(h_yards)
    v1 = convert_mph_to_fps(v_sand_mph)
    v2 = v1 / n

    def snell_equation(x: float) -> float:
        """Возвращает невязку уравнения Снеллиуса в точке x."""
        if x <= 0 or x >= h_ft:
            # Выходим за разумную область
            return 1e9

        sin_theta1 = x / math.sqrt(x * x + d1_ft * d1_ft)
        sin_theta2 = (h_ft - x) / math.sqrt((h_ft - x) * (h_ft - x) + d2_feet * d2_feet)

        return sin_theta1 * v2 - sin_theta2 * v1

    # Бисекция для поиска x, где snell_equation(x) = 0
    low, high = 1e-6, h_ft - 1e-6
    for _ in range(100):
        mid = (low + high) / 2.0
        val = snell_equation(mid)
        if val == 0:
            break
        elif val > 0:
            low = mid
        else:
            high = mid

    x_opt = (low + high) / 2.0
    theta1_opt = math.degrees(math.atan(x_opt / d1_ft))
    return theta1_opt

# Запуск программы
if __name__ == "__main__":
    main()