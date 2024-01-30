from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""

        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_MIN: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration_hour = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError(
            'Определите метод в %s.' % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,
            self.duration_hour,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Переопредление функции затраченных калорий."""

        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight_kg / self.M_IN_KM
            * self.duration_hour
            * self.H_IN_MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_1: float = 0.035
    K_2: float = 0.029
    SM_IN_M: int = 100
    KMH_IN_MS: float = 0.278

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height_cm = height

    def get_spent_calories(self) -> float:
        """Переопредление функции затраченных калорий."""

        return (
            (
                self.K_1 * self.weight_kg
                + ((self.get_mean_speed() * self.KMH_IN_MS)**2
                    / (self.height_cm / self.SM_IN_M))
                * self.K_2 * self.weight_kg
            )
            * self.duration_hour * self.H_IN_MIN
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    K_1: int = 2
    K_2: float = 1.1

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопредление функции средней скорости."""

        return (
            self.length_pool_m
            * self.count_pool
            / self.M_IN_KM
            / self.duration_hour
        )

    def get_spent_calories(self) -> float:
        """Переопредление функции затраченных калорий."""

        return (
            (
                self.get_mean_speed()
                + self.K_2
            )
            * self.K_1
            * self.weight_kg
            * self.duration_hour
        )


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_type_dict: dict[str, type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking
    }
    if workout_type not in workout_type_dict:
        raise KeyError(f'Нет типа данных {workout_type}')
    return workout_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
        ('SM', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
