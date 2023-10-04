from sqlalchemy import asc, create_engine, desc, func, select, text, update
from sqlalchemy.orm import Session

from ...database import models
from ...database.crud import users
from ...utils import actions as actions
from ...utils import logger
from ...utils import my_utils as utils
from ...utils.clockify_api import ClockifyApi

clockify = ClockifyApi()


# def sync_clockify_entries(db: Session, user_id, entries):
#     user = users.get_user(db, user=user_id)
#     logger.info("Sync entries for user " + str(user.name))
#     for entry in entries:
#         try:
#             start = entry["timeInterval"]["start"]
#             end = entry["timeInterval"]["end"]
#             duration = entry["timeInterval"]["duration"]
#             if end is None:
#                 end = ""
#             if duration is None:
#                 duration = ""
#             start = utils.change_timezone_clockify(start)
#             if end != "":
#                 end = utils.change_timezone_clockify(end)
#             project_name = clockify.get_project(entry["projectId"])["name"]
#             stmt = select(models.TimeEntries).where(
#                 models.TimeEntries.id == entry["id"]
#             )
#             exists = db.execute(stmt).first()
#             if not exists:
#                 new_entry = models.TimeEntries(
#                     id=entry["id"],
#                     user=user.name,
#                     user_id=user.id,
#                     user_clockify_id=user.clockify_id,
#                     project=project_name,
#                     project_id=entry["projectId"],
#                     start=start,
#                     end=end,
#                     duration=actions.convert_clockify_duration(duration),
#                 )
#                 db.add(new_entry)
#             else:
#                 stmt = (
#                     update(models.TimeEntries)
#                     .where(models.TimeEntries.id == entry["id"])
#                     .values(
#                         user=user.name,
#                         project=project_name,
#                         project_id=entry["projectId"],
#                         start=start,
#                         end=end,
#                         duration=actions.convert_clockify_duration(duration),
#                     )
#                 )
#                 db.execute(stmt)
#             db.commit()
#         except Exception as e:
#             db.rollback()
#             logger.info("Error adding new entry " + str(entry) + ": " + str(e))
#             raise e
#         # logger.info(entry["id"])
#         # exit()
#     return
