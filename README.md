# snowflake-task-state-to-slack
- Snowflakeで実行された最新のTaskの実行ステータスをSlackに通知するLambda関数。
- LambdaへのPython用のSnowflakeコネクターのインストールについては下記の通り。
  - Lambda Layersを使って追加。
  - レイヤーの追加方法は下記参照。
    - https://qiita.com/subretu/items/2a0c40326cc857e63922