from django.core.validators import RegexValidator


class UnicodeUsernameValidator(RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = (
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0
