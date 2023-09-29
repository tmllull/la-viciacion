import random

##########################
## Regular Achievements ##
##########################


def played_42_games(player):
    return (
        "*💥💥🏆🏆La respuesta🏆🏆💥💥*\n\n"
        + "*"
        + player
        + "* ha jugado a la mágica cifra de 42 juegos. "
        + "No sabemos si tendrá la respuesta al sentido de la vida, al universo y "
        + "todo lo demás, pero lo que seguro que tiene es mucho tiempo libre."
    )


def played_100_games(player):
    return (
        "*💥💥🏆🏆100 juegos (jugados)🏆🏆💥💥*\n\n"
        + "A 100 juegos acaba de jugar *"
        + player
        + "*."
        + " Estamos hablando de arrancar un nuevo juego cada 3,65 días. Pensemos en ello."
    )


def completed_42_games(player):
    return (
        "*💥💥🏆🏆La respuesta (de verdad)🏆🏆💥💥*\n\n"
        + "Si empezar 42 juegos ya es todo un logro, no hablemos de acabar 42. "
        + "Ha quedado patente que a *"
        + player
        + "* la vida más allá de la puerta de casa no le importa lo más mínimo."
    )


def played_8h_game_day(player, game):
    return (
        "*🏆Mi trabajo es jugar🏆*\n\n"
        + "Lo de estar 8 horas trabajando no suele gustar, pero jugando ya es otra cosa. "
        + "*"
        + player
        + "* acaba de cascarse 8 horas seguidas (o más) jugando a _"
        + game
        + "_; cualquira diría que le está gustando."
    )


def played_8h_day(player):
    return (
        "*🏆Una jornada laboral🏆*\n\n"
        + "Las jornadas laborales de 8 horas deberían desaparecer, pero no las de jugar. "
        + "*"
        + player
        + "* acaba de invertir el tiempo máximo legal para una jornada de trabajo."
    )


def played_12h_day(player):
    return (
        "*🏆Media jornada, 12 horas🏆*\n\n"
        + "Como decía 'El Rancio', media jornada son 12 horas, y ese es el tiempo que ha invertido "
        + "*"
        + player
        + "* en un solo día. Mariscos Recio estaría orgulloso."
    )


def played_16h_day(player):
    return (
        "💥💥🏆🏆No paro ni a cagar🏆🏆💥💥*\n\n"
        + "De las 24h del día, 8 se deberían dedicar a dormir, y las otras 16 a hacer cosas. "
        + "*"
        + player
        + "* ha deicidido invertirlas a jugar. Lo de comer y hacer otras necesidades como asearse ya para otro día."
    )


def played_less_5_min(player, game):
    return (
        "*🏆Lo he abierto sin querer🏆*\n\n"
        + "Al parecer _"
        + game
        + "_ no ha tenido mucho éxito para *"
        + player
        + "*, ya que ha hecho una ridícula sesión de juego de 5 minutos (o menos)."
    )


def played_100h_game(player, game):
    return (
        "*🏆Cualquiera diría que le gusta ese juego🏆*\n\n"
        + "Todo apunta a que _"
        + game
        + "_ ha enganchado a *"
        + player
        + "*, porque acaba de rebasar la barrera de las 100 horas invertidas en él."
    )


def played_5_games_day(player):
    return (
        "*🏆Indecisión🏆*\n\n"
        + "Este. No, este. No, mejor este otro. AAAHHHRRRGGG, tengo demasiados juegos. *"
        + player
        + "* no tiene ni idea de a qué jugar, y ya ha probado con 5 o más juegos en un solo día."
    )


def played_10_games_day(player):
    return (
        "*💥💥🏆🏆Indecisión x2🏆🏆💥💥*\n\n"
        + "AAAHHHRRRGGG, sigo sin saber a qué jugar. *"
        + player
        + "* ha acumulado tantos juegos en su biblioteca que salta de uno "
        + "a otro como pollo sin cabeza, y ya ha probado con 10 o más juegos en un solo día."
    )


def streak_7_days(player):
    return (
        "*🏆Racha de 7 días🏆*\n\n"
        + "Pues resulta que *"
        + player
        + "* lleva 1 semana jugando todos los días. "
        + "Podríamos decir que tiene pocas cosas mejores que hacer."
    )


def streak_15_days(player):
    return (
        "*🏆Racha de 15 días🏆*\n\n"
        + "Ya son 15 los días que lleva *"
        + player
        + "* sin faltar ni uno a la sesión de juego de rigor. "
        + "A este paso habrá que ir pensando en empezar a regarlo."
    )


def streak_30_days(player):
    return (
        "*🏆Racha de 30 días🏆*\n\n"
        + "Poco más que añadir. *"
        + player
        + "* acumula 30 días con una sesión de juego como mínimo. "
        + "Lo mejor será ir llamando al psiquiátrico."
    )


def streak_66_days(player):
    return (
        "*🏆Racha de 66 días🏆*\n\n"
        + "_Hábito, del latín habĭtus_. Dícese del modo especial de proceder "
        + "o conducirse adquirido por repetición de actos iguales o semejantes, "
        + "u originado por tendencias instintivas. "
        + "*"
        + player
        + "* acaba de comprobar que, según un estudio "
        + "(que me acabo de inventar), el hábito se consigue tras 66 días."
    )


def lose_streak(player, streak):
    msg = "❗⚠️" + player + " acaba de perder su racha de " + str(streak) + " días."
    msg += "⚠️❗"
    return msg


def break_streak(player, streak):
    return (
        "🎉" + player + " acaba de superar su mejor racha de " + str(streak) + " días.🎉"
    )


def just_in_time(player, game):
    return (
        "*🏆Justo a tiempo🏆*\n\n"
        + "*"
        + player
        + "* acaba de terminar _"
        + game
        + "_ exactamente en el tiempo medio según HLTB."
    )


############
## Others ##
############


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


def silksong_message():
    messages = [
        "Sale antes un Zelda en PC que el Silksong.",
        "¿Silksong? 😂😂😂😂.",
        "Cuando los de FromSoftware añadan un modo fácil a lo mejor sale el Silksong.",
        "¿Te dice algo la palabra 'Abandoned'?",
        "Por más que lo nombres no saldrá antes.",
        "No sé de qué hablas, pero es leer Silksong y se me saltan las lágrimas (pero de la risa).",
    ]
    return random.choice(messages)


def sanderson_message(user):
    messages = [
        "😠",
        "🤨",
        user + " frunció el ceño mientras decía eso.",
        "Dijo " + user + " con el ceño fruncido.",
        "Soltó " + user + " mientras fruncía el ceño.",
        "Dijo " + user + " frunciendo el ceño.",
    ]
    return random.choice(messages)


def bot_not_works_message(user):
    messages = [
        "¿Qué hablas? A ver si vas a ser tú que no tienes ni puta idea.",
        "Menos quejas y más comprensión. Uno hace lo que puede, ¿vale?",
        "Mucha queja pero poco aporte.",
        "Lo de 'crítica constructiva' no está en tu vocabulario, ¿no?",
        "Cállate.",
        "Vaya, ahora " + user + " va de guay. Ponte tú a hacerlo y luego me cuentas.",
        "Bla, bla, bla. Sólo quejas",
        "¿Y? ¿Acaso tú no te equivocas nunca?",
        "Pues hazlo tú.",
        "Qué fácil es criticar el trabajo de los demás.",
    ]
    return random.choice(messages)
