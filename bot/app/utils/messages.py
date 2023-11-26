import random

forbiden = (
    "Ande vas, Barrabás. No estás autorizado para usar "
    + "este bot. Habla con mi creador, a mi no me mires."
)


def start(name):
    return (
        "Hola *"
        + name
        + "*, soy el bot de 'La Viciación'. "
        + "Para saber la lista de comandos disponibles escribe /help, pero "
        + "si quieres usarlos es necesario que tengas un nick en Telegram (y se "
        + "lo comuniques mi creador para que te añada a la lista de personas humanas fiables)."
    )
