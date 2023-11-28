from telegram import InlineKeyboardButton

EXIT = "❌ Salir"

ACTIVATE_ACCOUNT = [
    [
        InlineKeyboardButton("🔓 Activa tu cuenta", callback_data="activate_account"),
    ],
    [
        InlineKeyboardButton(EXIT, callback_data="cancel"),
    ],
]

MAIN_MENU = [
    [
        InlineKeyboardButton("🕺 Mis estadísticas", callback_data="my_data"),
        InlineKeyboardButton("🏅 Rankings", callback_data="rankings"),
    ],
    [
        # InlineKeyboardButton("🕹 ¿A qué puedo jugar?", callback_data="recommender"),
        InlineKeyboardButton("📎 Actualizar info", callback_data="update_info"),
        InlineKeyboardButton("🔎 Info juego", callback_data="info_game"),
    ],
    # [
    # InlineKeyboardButton("📎 Actualizar info", callback_data="update_info"),
    # InlineKeyboardButton("✅ Estado del servicio", callback_data="status"),
    # ],
    [
        InlineKeyboardButton(EXIT, callback_data="cancel"),
    ],
]

ADMIN_MENU = [
    [
        InlineKeyboardButton("🕺 Mis estadísticas", callback_data="my_data"),
        InlineKeyboardButton("🏅 Rankings", callback_data="rankings"),
    ],
    [
        # InlineKeyboardButton("🕹 ¿A qué puedo jugar?", callback_data="recommender"),
        InlineKeyboardButton("🔎 Info juego", callback_data="info_game"),
    ],
    [
        InlineKeyboardButton("📎 Actualizar info", callback_data="update_info"),
        InlineKeyboardButton("✅ Estado del servicio", callback_data="status"),
    ],
    [
        InlineKeyboardButton(EXIT, callback_data="cancel"),
    ],
    [
        InlineKeyboardButton("🔎 Usuarios", callback_data="get_users"),
        InlineKeyboardButton("📢 Enviar notificación", callback_data="send_message"),
    ],
]


MY_DATA = [
    [
        InlineKeyboardButton("🎮 Juegos", callback_data="my_games"),
        InlineKeyboardButton("✅ Completados", callback_data="my_completed_games"),
    ],
    [
        InlineKeyboardButton("⏳ Top juegos", callback_data="my_top_games"),
        InlineKeyboardButton("🥇 Logros", callback_data="my_achievements"),
    ],
    [
        InlineKeyboardButton("✨ Racha", callback_data="my_streak"),
    ],
    [
        InlineKeyboardButton("🔙 Atrás", callback_data="back"),
        InlineKeyboardButton(EXIT, callback_data="cancel"),
    ],
]

RANKING_MENU = [
    [
        InlineKeyboardButton("📅 Días", callback_data="ranking_days"),
        InlineKeyboardButton("⌚ Horas", callback_data="ranking_hours"),
    ],
    [
        InlineKeyboardButton("🎮 Jugados", callback_data="ranking_played"),
        InlineKeyboardButton("✅ Completados", callback_data="ranking_completed"),
    ],
    [
        InlineKeyboardButton("🥇 Logros", callback_data="ranking_achievements"),
        InlineKeyboardButton("🆚 Ratio", callback_data="ranking_ratio"),
    ],
    [
        InlineKeyboardButton("✨ R. actual", callback_data="ranking_current_streak"),
        InlineKeyboardButton("⭐ R. máx.", callback_data="ranking_streak"),
    ],
    [
        InlineKeyboardButton("💸 Deuda técnica", callback_data="ranking_debt"),
        InlineKeyboardButton(
            "🆕 Últimos jugados", callback_data="ranking_last_played_games"
        ),
    ],
    [
        InlineKeyboardButton("🏟️ Más jugados", callback_data="ranking_most_played"),
        # InlineKeyboardButton("🖥 Plataforma", callback_data="ranking_platform"),
    ],
    [
        InlineKeyboardButton("🔙 Atrás", callback_data="back"),
        InlineKeyboardButton(EXIT, callback_data="cancel"),
    ],
]

YES_NO = [["✅ Sí", "❌ No"]]

EXCEL_ACTIONS = [
    ["🆕 Añadir juego", "⏲ Añadir tiempo"],
    ["✅ Completar juego", "📝 Puntuar juego"],
    ["▶️ Activar timer", "⏹ Parar timer"],
    [EXIT],
]

CANCEL = [EXIT]
