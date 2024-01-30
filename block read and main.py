for book_type in workout_type_dict:
    if book_type == workout_type:
        return workout_type_dict[workout_type](*data)
    else:
        return KeyError('sss')
    



    def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_type_dict: dict[str, type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking
    }
    try:
        return workout_type_dict[workout_type](*data)
    except KeyError:
        print('g')


def main(training: Training) -> None:
    """Главная функция."""
    try:

        info: InfoMessage = training.show_training_info()
        print(info.get_message())
    except TypeError:
        print('ssss')