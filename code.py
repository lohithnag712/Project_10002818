import logging

from quart import Blueprint, abort, current_app, request

from webhook.decorators import verify_request_signature

logger = logging.getLogger("quart.serving")

webhook = Blueprint("webhook", __name__)


@webhook.get("/webhook")
@verify_request_signature
async def verify():
    mode: str = request.args.get("hub.mode", "")
    verify_token: str = request.args.get("hub.verify_token", "")

    WEBHOOK_VERIFY_TOKEN: str = current_app.config["WEBHOOK_VERIFY_TOKEN"]

    if (mode and verify_token) and (
        mode == "subscribe" and verify_token == WEBHOOK_VERIFY_TOKEN
    ):
        logger.info("Webhook verified.")

        return (request.args.get("hub.challenge"), 200)
    else:
        abort(403)


@webhook.post("/webhook")
@verify_request_signature
async def listen():
    body = await request.get_json()

    logger.info("Webhook received.", extra=body)

    return ("EVENT_RECEIVED", 200)