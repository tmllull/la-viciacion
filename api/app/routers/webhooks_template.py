from fastapi import APIRouter, Request
from fastapi_versioning import version

from ..utils import actions as actions
from ..utils.logger import LogManager

log_manager = LogManager()
logger = log_manager.get_logger()


router = APIRouter(
    prefix="/webhooks", tags=["Webhooks"], responses={404: {"description": "Not found"}}
)


@router.get("/123456789")
@version(1)
def webhook_test(request: Request):
    """This webhook appears in docs page"""
    return {"message": "Webhook received", "request": request}


@router.get("/987654321", include_in_schema=False)
@version(1)
def webhook_test2(request: Request):
    """This webhook NOT appears in docs page, because of 'include_in_schema=False'"""
    return {"message": "Webhook received", "request": request}
