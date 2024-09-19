import time


class SomeModel:
    def predict(self, message: str) -> float:
        print(f'start predicting with {message=}')
        time.sleep(3)
        return 999

    def some_method(self):
        # pylint ругается на слишком малое количество методов
        pass


def predict_message_mood(
        message: str,
        bad_thresholds: float = 0.3,
        good_thresholds: float = 0.8,
) -> str:
    if good_thresholds <= bad_thresholds:
        raise ValueError("bad_thresholds should be less then good_thresholds")

    model = SomeModel()
    result = model.predict(message)
    if result < bad_thresholds:
        return "неуд"
    if result > good_thresholds:
        return "отл"
    return "норм"
