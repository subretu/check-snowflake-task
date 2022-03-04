# snowflake-task-state-slack-notification
- Python用のSnowflakeコネクターのインストール。
  - Lambda Layersを使って追加。
  - レイヤーの追加方法は下記参照。
    - https://qiita.com/subretu/items/2a0c40326cc857e63922
- Snowflakeのtask履歴抽出のSQLにおける下記変数は自分の環境に合わせること。
  ```
  DATABASENAME
  ```