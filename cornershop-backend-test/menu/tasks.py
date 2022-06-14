import json

from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings

import requests

logger = get_task_logger(__name__)


def send_slack_message(text="", channel="", auth=""):
    """
    Sends a text message to a specific Slack channel using Token authentication
    """
    url = "https://slack.com/api/chat.postMessage"
    slack_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        "channel": channel,
        "text": text,
    }
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + auth}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    return response


@task()
def send_Slack_menu_reminder(menu_url):
    """
    Sends menu reminder (URL) to all employees
    that are members of the Slack channel.
    """
    logger.info("Sent slack reminder")
    text = (
        "Hello! \n I share with you today's menu :)"
        + f"\n {menu_url} \n Have a nice day!"
    )
    send_slack_message(
        text=text, channel=settings.SLACK_CHANNEL, auth=settings.SLACK_TOKEN
    )
