import telegram
import telegram.ext.filters as FILTERS
from dotenv import dotenv_values
from routes.admin_routes import AdminRoutes
from routes.basic_routes import BasicRoutes
from routes.excel_routes import ExcelRoutes
from routes.my_routes import MyRoutes
from routes.other_routes import OtherRoutes
from routes.ranking_routes import RankingRoutes
from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from utils.config import Config
from utils.my_utils import MyUtils

##########
## INIT ##
##########

utils = MyUtils()
config = Config()
my_routes = MyRoutes()
basic_routes = BasicRoutes()
ranking_routes = RankingRoutes()
admin_routes = AdminRoutes()
other_routes = OtherRoutes()
excel_routes = ExcelRoutes()

FILTER_YES = "^(✅ Sí)$"
FILTER_NO = "^(❌ No)$"
FILTER_EXIT = "^(❌ Salir)$"


async def post_init(application: Application):
    await application.bot.set_my_commands(
        [
            BotCommand("/start", "Iniciar el chat"),
            BotCommand("/menu", "Menú principal"),
            BotCommand("/help", "Ayuda"),
        ]
    )


def main() -> None:
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).post_init(post_init).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("menu", basic_routes.menu)],
        states={
            utils.MAIN_MENU: [
                CallbackQueryHandler(my_routes.my_data, pattern="^" + "my_data" + "$"),
                CallbackQueryHandler(
                    ranking_routes.rankings, pattern="^" + "rankings" + "$"
                ),
                # CallbackQueryHandler(
                #     other_routes.recommender, pattern="^" + "recommender" + "$"
                # ),
                CallbackQueryHandler(
                    other_routes.info_game, pattern="^" + "info_game" + "$"
                ),
                CallbackQueryHandler(
                    admin_routes.send_message, pattern="^" + "send_message" + "$"
                ),
                CallbackQueryHandler(
                    admin_routes.get_users, pattern="^" + "get_users" + "$"
                ),
                CallbackQueryHandler(
                    excel_routes.update_info, pattern="^" + "update_info" + "$"
                ),
                CallbackQueryHandler(basic_routes.status, pattern="^" + "status" + "$"),
                CallbackQueryHandler(basic_routes.end, pattern="^" + "cancel" + "$"),
            ],
            utils.INFO_GAME: [
                MessageHandler(None, other_routes.info_game_response),
            ],
            utils.MY_ROUTES: [
                CallbackQueryHandler(
                    my_routes.my_games, pattern="^" + "my_games" + "$"
                ),
                CallbackQueryHandler(
                    my_routes.my_completed_games,
                    pattern="^" + "my_completed_games" + "$",
                ),
                CallbackQueryHandler(
                    my_routes.my_achievements, pattern="^" + "my_achievements" + "$"
                ),
                CallbackQueryHandler(
                    my_routes.my_top_games, pattern="^" + "my_top_games" + "$"
                ),
                CallbackQueryHandler(
                    my_routes.my_streak, pattern="^" + "my_streak" + "$"
                ),
                CallbackQueryHandler(basic_routes.back, pattern="^" + "back" + "$"),
                CallbackQueryHandler(basic_routes.end, pattern="^" + "cancel" + "$"),
            ],
            utils.RANKING_ROUTES: [
                # CallbackQueryHandler(
                #     ranking_routes.ranking_rated_games,
                #     pattern="^" + "ranking_rated_games" + "$",
                # ),
                CallbackQueryHandler(
                    ranking_routes.ranking_achievements,
                    pattern="^" + "ranking_achievements" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_completed,
                    pattern="^" + "ranking_completed" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_days, pattern="^" + "ranking_days" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_hours, pattern="^" + "ranking_hours" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_played, pattern="^" + "ranking_played" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_ratio, pattern="^" + "ranking_ratio" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_streak, pattern="^" + "ranking_streak" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_debt, pattern="^" + "ranking_debt" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_last_played_games,
                    pattern="^" + "ranking_last_played_games" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_most_played,
                    pattern="^" + "ranking_most_played" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.ranking_current_streak,
                    pattern="^" + "ranking_current_streak" + "$",
                ),
                # CallbackQueryHandler(
                #     ranking_routes.ranking_platform,
                #     pattern="^" + "ranking_platform" + "$",
                # ),
                CallbackQueryHandler(basic_routes.back, pattern="^" + "back" + "$"),
                CallbackQueryHandler(basic_routes.end, pattern="^" + "cancel" + "$"),
            ],
            utils.SEND_MESSAGE: [
                CommandHandler("cancel", admin_routes.send_message_action),
                MessageHandler(
                    filters.Regex(FILTER_YES), admin_routes.send_message_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), admin_routes.send_message_confirmation
                ),
                MessageHandler(None, admin_routes.send_message_action),
            ],
            utils.EXCEL_STUFF: [
                MessageHandler(
                    filters.Regex("^(🆕 Añadir juego)$"), excel_routes.add_game
                ),
                MessageHandler(
                    filters.Regex("^(⏲ Añadir tiempo)$"), excel_routes.update_time
                ),
                MessageHandler(
                    filters.Regex("^(✅ Completar juego)$"), excel_routes.complete_game
                ),
                MessageHandler(
                    filters.Regex("^(📝 Puntuar juego)$"), excel_routes.rate_game
                ),
                MessageHandler(
                    filters.Regex("^(▶️ Activar timer)$"), excel_routes.active_timer
                ),
                MessageHandler(
                    filters.Regex("^(⏹ Parar timer)$"), excel_routes.stop_timer
                ),
                MessageHandler(filters.Regex(FILTER_EXIT), excel_routes.cancel_excel),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
            utils.EXCEL_TIME_SELECT_GAME: [
                MessageHandler(filters.Regex(FILTER_EXIT), excel_routes.cancel_excel),
                MessageHandler(None, excel_routes.update_time_game_select),
            ],
            utils.EXCEL_ADD_TIME: [
                MessageHandler(None, excel_routes.update_time_time_select),
            ],
            utils.EXCEL_CONFIRM_TIME: [
                MessageHandler(
                    filters.Regex(FILTER_YES), excel_routes.update_time_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), excel_routes.update_time_confirmation
                ),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
            utils.EXCEL_COMPLETE_GAME: [
                MessageHandler(filters.Regex(FILTER_EXIT), excel_routes.cancel_excel),
                MessageHandler(None, excel_routes.complete_game_validation),
            ],
            utils.EXCEL_CONFIRM_COMPLETED: [
                MessageHandler(
                    filters.Regex(FILTER_YES), excel_routes.complete_game_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), excel_routes.complete_game_confirmation
                ),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
            utils.EXCEL_ADD_GAME: [
                MessageHandler(None, excel_routes.add_game_get_name),
            ],
            utils.EXCEL_ADD_GAME_PLATFORM: [
                MessageHandler(None, excel_routes.add_game_validation),
            ],
            utils.EXCEL_ADD_GAME_CONFIRMATION: [
                MessageHandler(
                    filters.Regex(FILTER_YES), excel_routes.add_game_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), excel_routes.add_game_confirmation
                ),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
            utils.EXCEL_RATE_GAME: [
                MessageHandler(filters.Regex(FILTER_EXIT), excel_routes.cancel_excel),
                MessageHandler(None, excel_routes.rate_game_get_name),
            ],
            utils.EXCEL_RATE_GAME_RATING: [
                MessageHandler(None, excel_routes.rate_game_get_rating),
            ],
            utils.EXCEL_CONFIRM_RATE: [
                MessageHandler(
                    filters.Regex(FILTER_YES), excel_routes.add_rating_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), excel_routes.add_rating_confirmation
                ),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
            utils.EXCEL_START_TIMER: [
                MessageHandler(filters.Regex(FILTER_EXIT), excel_routes.cancel_excel),
                MessageHandler(None, excel_routes.active_timer_validation),
            ],
            utils.EXCEL_START_TIMER_COMPLETED: [
                MessageHandler(
                    filters.Regex(FILTER_YES), excel_routes.active_timer_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), excel_routes.active_timer_confirmation
                ),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
            utils.EXCEL_STOP_TIMER: [
                MessageHandler(
                    filters.Regex(FILTER_YES), excel_routes.stop_timer_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), excel_routes.stop_timer_confirmation
                ),
                MessageHandler(None, excel_routes.cancel_excel),
            ],
        },
        fallbacks=[CommandHandler("menu", basic_routes.menu)],
        per_user=True,
        conversation_timeout=60,
    )
    app.add_handler(CommandHandler("info_dev", utils.info_dev))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", utils.start))
    app.add_handler(CommandHandler("help", utils.help))
    app.add_handler(MessageHandler(None, other_routes.random_response))

    app.run_polling()


if __name__ == "__main__":
    main()
