- deploy時の切り戻しを簡易にしたい -> 2系統運用
| - master
| - premaster
| - migration上の都合で一気に出さないといけないことがある
|   - リリース方法をえらべるようにする
|     - fast mode ()
|     - slow mode ()
- performance testが実行された状態のものをdeployしたい
| - stagin でperformance testを実行する
- aging testが実行された状態のものをdeployしたい
| - staging でaging testを実行する
| - aging test時にも外部system連携する

master
^
| human decision
| - manual deploy
| - schedule deploy
premaster - deploy test and slow deploy
^
| auto deploy
| - no migration only
| - migrationがある場合は手動実行する
| -
staging - aging testing and final check and demo
^
| auto deploy
| - performance test ok [NewRelic, Funkload]
| - aging test ok [selenium]
| - collaboration other service
develop
^
| auto merge
| - lint ok [flake8, pylint]
| - compile ok [python]
| - unittest ok [nose, pytest]
| - documentation build ok [sphinx]
| - coverage 100% [coverage]
| - auto deploy ok [chef, ansible, docker]
| - migration test ok [alembic, django.migration]
| - add document ok [pylint]
| - basic test (not unittest) []
| - comment lgmt
| - no wip title
topic
