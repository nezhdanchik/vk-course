import time


class SomeModel:
    def predict(self, message: str) -> float:
        time.sleep(3)
        return 999


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
    elif result > good_thresholds:
        return "отл"
    else:
        return "норм"
