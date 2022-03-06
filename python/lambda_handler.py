import os
import json
import urllib.request
import snowflake_infomation


SLACK_URL = os.environ.get("SLACK_URL")


def post_slack(url, is_success, msg=""):
    if is_success:
        text = "Snowflake task state"
    else:
        text = "Lambda execution fails（snowflake task state to slack）"

    if msg != "":
        text += f":\n```{msg}```"

    headers = {"Content-Type": "application/json"}
    data = {"text": text}

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req):
        pass

    return


def lambda_handler(event, context):
    try:
        snowflake_meta = snowflake_infomation.MetaData()
        msg = snowflake_meta.get_latest_task_state()
        if SLACK_URL is not None:
            post_slack(SLACK_URL, True, msg)
    except BaseException as e:
        if SLACK_URL is not None:
            msg = type(e).__name__
            if str(e) != "":
                msg += ": "
                msg += str(e)
            post_slack(SLACK_URL, False, msg)
        raise e
