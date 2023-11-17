import allure


def GIVEN(title):
    return GWT("GIVEN", title)


def WHEN(title):
    return GWT("WHEN", title)


def THEN(title):
    return GWT("THEN", title)


class GWT:
    def __init__(self, step_type, title):
        self.title = title
        self.step_type = step_type

    def __enter__(self):
        self.main_step_context = allure.step(self.step_type)
        self.nested_step_context = allure.step(self.title)
        self.main_step_context.__enter__()
        self.nested_step_context.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.nested_step_context.__exit__(exc_type, exc_val, exc_tb)
        self.main_step_context.__exit__(exc_type, exc_val, exc_tb)
