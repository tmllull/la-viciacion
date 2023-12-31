import telegram
import telegram.ext.filters as FILTERS
from dotenv import dotenv_values
from routes.admin_routes import AdminRoutes
from routes.basic_routes import BasicRoutes
from routes.data_routes import DataRoutes
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
data_routes = DataRoutes()

FILTER_YES = "^(✅ Sí)$"
FILTER_NO = "^(❌ No)$"
FILTER_EXIT = "^(❌ Salir)$"


async def post_init(application: Application):
    await application.bot.set_my_commands(
        [
            BotCommand("/start", "Iniciar el chat"),
            BotCommand("/menu", "Menú principal"),
            BotCommand("/activate", "Activar cuenta"),
            BotCommand("/help", "Ayuda"),
        ]
    )


def main() -> None:
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).post_init(post_init).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("menu", basic_routes.menu),
            CommandHandler("activate", basic_routes.activate_account),
        ],
        states={
            utils.ACTIVATE_ACCOUNT: [
                # MessageHandler(None, basic_routes.activate_account_validation),
                CallbackQueryHandler(
                    basic_routes.activate_account_validation,
                    pattern="^" + "activate_account" + "$",
                ),
                CallbackQueryHandler(basic_routes.end, pattern="^" + "cancel" + "$"),
            ],
            utils.MAIN_MENU: [
                CallbackQueryHandler(my_routes.my_data, pattern="^" + "my_data" + "$"),
                CallbackQueryHandler(
                    ranking_routes.rankings, pattern="^" + "rankings" + "$"
                ),
                # CallbackQueryHandler(
                #     other_routes.recommender, pattern="^" + "recommender" + "$"
                # ),
                # CallbackQueryHandler(
                #     other_routes.info_game, pattern="^" + "info_game" + "$"
                # ),
                CallbackQueryHandler(
                    admin_routes.send_message, pattern="^" + "send_message" + "$"
                ),
                # CallbackQueryHandler(
                #     admin_routes.get_users, pattern="^" + "get_users" + "$"
                # ),
                CallbackQueryHandler(
                    data_routes.update_data, pattern="^" + "update_data" + "$"
                ),
                # CallbackQueryHandler(basic_routes.status, pattern="^" + "status" + "$"),
                CallbackQueryHandler(basic_routes.end, pattern="^" + "cancel" + "$"),
            ],
            # utils.INFO_GAME: [
            #     MessageHandler(None, other_routes.info_game_response),
            # ],
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
                    ranking_routes.user_achievements,
                    pattern="^" + "user_achievements" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.user_completed_games,
                    pattern="^" + "user_completed_games" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.user_days,
                    pattern="^" + "user_days" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.user_hours,
                    pattern="^" + "user_hours" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.user_played_games,
                    pattern="^" + "user_played_games" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.user_ratio, pattern="^" + "user_ratio" + "$"
                ),
                CallbackQueryHandler(
                    ranking_routes.user_best_streak,
                    pattern="^" + "user_best_streak" + "$",
                ),
                CallbackQueryHandler(ranking_routes.debt, pattern="^" + "debt" + "$"),
                CallbackQueryHandler(
                    ranking_routes.games_last_played,
                    pattern="^" + "games_last_played" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.games_most_played,
                    pattern="^" + "games_most_played" + "$",
                ),
                CallbackQueryHandler(
                    ranking_routes.user_current_streak,
                    pattern="^" + "user_current_streak" + "$",
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
                    filters.Regex("^(🆕 Empezar juego)$"), data_routes.add_game
                ),
                # MessageHandler(
                #     filters.Regex("^(⏲ Añadir tiempo)$"), data_routes.add_time
                # ),
                MessageHandler(
                    filters.Regex("^(✅ Completar juego)$"), data_routes.complete_game
                ),
                MessageHandler(
                    filters.Regex("^(📝 Puntuar juego)$"), data_routes.rate_game
                ),
                # MessageHandler(
                #     filters.Regex("^(▶️ Activar timer)$"), data_routes.active_timer
                # ),
                # MessageHandler(
                #     filters.Regex("^(⏹ Parar timer)$"), data_routes.stop_timer
                # ),
                MessageHandler(filters.Regex(FILTER_EXIT), data_routes.cancel_data),
                MessageHandler(None, data_routes.cancel_data),
            ],
            # utils.EXCEL_TIME_SELECT_GAME: [
            #     MessageHandler(filters.Regex(FILTER_EXIT), data_routes.cancel_data),
            #     MessageHandler(None, data_routes.add_time_game_select),
            # ],
            # utils.EXCEL_ADD_TIME: [
            #     MessageHandler(None, data_routes.add_time_time_select),
            # ],
            # utils.EXCEL_CONFIRM_TIME: [
            #     MessageHandler(
            #         filters.Regex(FILTER_YES), data_routes.add_time_confirmation
            #     ),
            #     MessageHandler(
            #         filters.Regex(FILTER_NO), data_routes.add_time_confirmation
            #     ),
            #     MessageHandler(None, data_routes.cancel_data),
            # ],
            utils.EXCEL_COMPLETE_GAME: [
                MessageHandler(filters.Regex(FILTER_EXIT), data_routes.cancel_data),
                MessageHandler(None, data_routes.complete_game_validation),
            ],
            utils.EXCEL_CONFIRM_COMPLETED: [
                MessageHandler(
                    filters.Regex(FILTER_YES), data_routes.complete_game_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), data_routes.complete_game_confirmation
                ),
                MessageHandler(None, data_routes.cancel_data),
            ],
            utils.EXCEL_ADD_GAME: [
                MessageHandler(None, data_routes.add_game_get_name),
            ],
            utils.EXCEL_ADD_GAME_PLATFORM: [
                MessageHandler(None, data_routes.add_game_validation),
            ],
            utils.EXCEL_ADD_GAME_CONFIRMATION: [
                MessageHandler(
                    filters.Regex(FILTER_YES), data_routes.add_game_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), data_routes.add_game_confirmation
                ),
                MessageHandler(None, data_routes.cancel_data),
            ],
            utils.EXCEL_RATE_GAME: [
                MessageHandler(filters.Regex(FILTER_EXIT), data_routes.cancel_data),
                MessageHandler(None, data_routes.rate_game_get_name),
            ],
            utils.EXCEL_RATE_GAME_RATING: [
                MessageHandler(None, data_routes.rate_game_get_rating),
            ],
            utils.EXCEL_CONFIRM_RATE: [
                MessageHandler(
                    filters.Regex(FILTER_YES), data_routes.add_rating_confirmation
                ),
                MessageHandler(
                    filters.Regex(FILTER_NO), data_routes.add_rating_confirmation
                ),
                MessageHandler(None, data_routes.cancel_data),
            ],
            # utils.EXCEL_START_TIMER: [
            #     MessageHandler(filters.Regex(FILTER_EXIT), data_routes.cancel_data),
            #     MessageHandler(None, data_routes.active_timer_validation),
            # ],
            # utils.EXCEL_START_TIMER_COMPLETED: [
            #     MessageHandler(
            #         filters.Regex(FILTER_YES), data_routes.active_timer_confirmation
            #     ),
            #     MessageHandler(
            #         filters.Regex(FILTER_NO), data_routes.active_timer_confirmation
            #     ),
            #     MessageHandler(None, data_routes.cancel_data),
            # ],
            # utils.EXCEL_STOP_TIMER: [
            #     MessageHandler(
            #         filters.Regex(FILTER_YES), data_routes.stop_timer_confirmation
            #     ),
            #     MessageHandler(
            #         filters.Regex(FILTER_NO), data_routes.stop_timer_confirmation
            #     ),
            #     MessageHandler(None, data_routes.cancel_data),
            # ],
        },
        fallbacks=[CommandHandler("menu", basic_routes.menu)],
        per_user=True,
        conversation_timeout=60,
    )
    app.add_handler(CommandHandler("info_dev", utils.info_dev))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", utils.start))
    # app.add_handler(CommandHandler("activate", basic_routes.activate_account))
    app.add_handler(CommandHandler("help", utils.help))
    # app.add_handler(MessageHandler(None, other_routes.random_response))

    app.run_polling()


if __name__ == "__main__":
    main()
