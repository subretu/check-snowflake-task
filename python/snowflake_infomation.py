import os
import configparser
import snowflake.connector


class MetaData:
    def __init__(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read("./config.ini", encoding="utf-8")

    def get_latest_task_state(self):
        conn = snowflake.connector.connect(
            user=os.environ.get("user"),
            password=os.environ.get("pass"),
            account=os.environ.get("account"),
        )
        cur = conn.cursor()
        taskname = self.config_ini.get("Task", "taskname")

        try:
            sql = f"""
                  with task as (
                      select
                          name
                          ,state
                          ,rank() over (partition by name order by query_start_time desc) as rank
                      from
                          --DATABASENAMEは自分の環境のDB名にすること
                          table (DATABASENAME.information_schema.task_history ())
                      where
                          name in ({taskname})
                          and
                          query_id is not null
                  )
                  select
                      name
                      ,state
                  from
                      task
                  where
                      rank = 1
                  ;
            """
            cur.execute(sql)
            result_row = cur.fetchall()
            msg = ""
            for row in result_row:
                if row[1] == "FAILED":
                    msg += (
                        f"{row[0]} : {row[1]}（ERROR_CODE:{row[2]} ERROR_MESSAGE:{row[3]}）"
                        + "\n"
                    )
                msg += f"{row[0]} : {row[1]}" + "\n"
        finally:
            cur.close()
            conn.close()

            return msg
