from datetime import datetime, timedelta, timezone
import snowflake.connector
import os
import json
import configparser
import urllib.request


SLACK_URL = os.environ.get("SLACK_URL")


def post_slack(url, is_success, msg=""):
    if is_success:
        text = "Snowflake task is SUCCESS"
    else:
        text = "<!channel> Snowflake task is FAILURE"

    if msg != "":
        text += f":\n```{msg}```"

    headers = {"Content-Type": "application/json"}
    data = {"text": text}

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req):
        pass

    return


def get_task_status():
    conn = snowflake.connector.connect(
        user=os.environ.get("user"),
        password=os.environ.get("pass"),
        account=os.environ.get("account"),
    )
    cur = conn.cursor()

    config_ini = configparser.ConfigParser()
    config_ini.read("./config.ini", encoding='utf-8')
    taskname = config_ini.get("Task", "taskname")

    try:
        sql = f"""
        with a1 as (
        	select
        		name
        		,state
        		,rank() over (partition by name order by query_start_time desc) as rank
        	from
        		table (DATABASENAME.information_schema.task_history ())
        	where
            --対象のtask名
        		name in ({taskname})
        		and
        		query_id is not null
        )
        select
        	name, state
        from
        	a1
        where
        	rank = 1
        ;
        """
        cur.execute(sql)
        result_row = cur.fetchall()
        msg = ""
        for row in result_row:
            msg += f"{row[0]} : {row[1]}" + "\n"

    finally:
        cur.close()
        conn.close()

        return msg


def lambda_handler(event, context):
    try:
        msg = get_task_status()
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
