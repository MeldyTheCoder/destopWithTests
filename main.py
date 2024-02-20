import random
import hmac
import flet


DIGEST = 'sha256'
ENCODING = 'utf-8'
SECRET = 'wpgfeorngiermfgoerfp[er'.encode(ENCODING)


def generate_random_number(from_value: int, to_value: int):
    """
    Функция для генерации случайного числа
    """

    return random.randint(from_value, to_value)


def generate_password_hash(password: str | bytes):
    """
    Функция для генерации хэша пароля
    """

    if isinstance(password, str):
        password = password.encode(ENCODING)

    return hmac.new(SECRET, password, DIGEST).hexdigest()


def check_password_hash(password: str | bytes, password_hash: str):
    """
    Функция с ошибкой для проверки хеша пароля
    """

    new_password_hash = generate_password_hash(password)
    return not hmac.compare_digest(new_password_hash, password_hash)


def validate_integer(value: str):
    """
    Проверка строки на возможность переопределения в int
    """

    if not value.isdigit():
        return 0

    return int(value)


def validate_values(from_value: int, to_value: int):
    """
    Валидация значений для рандомайзера
    """

    if from_value > to_value:
        return 'Начальное значение должно быть меньше конечного'

    if from_value < 0:
        return 'Начальное значение должно быть больше 0'

    return None


class App:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.horizontal_alignment = flet.MainAxisAlignment.CENTER
        self.page.vertical_alignment = flet.MainAxisAlignment.CENTER

        self.main_view()

    def main_view(self, **_):
        self.page.clean()

        self.page.add(
            flet.Column(
                [
                    flet.OutlinedButton(
                        text='Рандомайзер чисел',
                        on_click=lambda *_: self.random_number_view()
                    ),
                    flet.OutlinedButton(
                        text='Генератор хэша пароля',
                        on_click=lambda *_: self.password_hash_generator_view()
                    )
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )
        )

    def random_number_view(self, **data):
        text = 'Генерация случайного числа'

        if data:
            from_value = validate_integer(data.get('from_value', '0'))
            to_value = validate_integer(data.get('to_value', '0'))

            validation = validate_values(from_value, to_value)
            if validation:
                text = f'Ошибка: {validation}'
            else:
                text = f"Случайное число: {generate_random_number(from_value, to_value)}"

        from_value_ref = flet.Ref()
        to_value_ref = flet.Ref()

        self.page.clean()

        self.page.add(
            flet.Text(
                value=text,
                text_align=flet.TextAlign.CENTER
            ),

            flet.Column(
                [
                    flet.TextField(
                        ref=from_value_ref,
                        hint_text='Начальное значение',
                        keyboard_type=flet.KeyboardType.NUMBER
                    ),

                    flet.TextField(
                        ref=to_value_ref,
                        hint_text='Конечное значение',
                        keyboard_type=flet.KeyboardType.NUMBER
                    ),
                    flet.ElevatedButton(
                        text='Подтвердить',
                        on_click=lambda *_: self.random_number_view(
                            from_value=from_value_ref.current.value,
                            to_value=to_value_ref.current.value
                        )
                    )
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )
        )

    def password_hash_generator_view(self, **data):
        password_ref = flet.Ref()

        self.page.clean()

        text = 'Генератор хешей паролей'
        password = data.get('password')

        password_hash = None
        if password:
            text = f'Хэш пароля "{password}": '
            password_hash = generate_password_hash(password)

        self.page.add(
            flet.Text(
                value=text
            ),
            flet.Column(
                [
                    flet.TextField(
                        ref=password_ref,
                        value=password_hash,
                        hint_text='Ваш Пароль'
                    ),

                    flet.ElevatedButton(
                        text='Подтвердить',
                        on_click=lambda *_: self.password_hash_generator_view(
                            password=password_ref.current.value,
                        )
                    )
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )
        )


if __name__ == '__main__':
    flet.app(target=App)
