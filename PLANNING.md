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


stable
^
|
master -> current release
^
| git-pr-release
develop [auto deploy] -> aging and qa
^
| auto merge
topic


開発作業
- issueを作成 `git issue create -m "issue title"`
- topic branchを作成 `git checkout -b USERNAME-ISSUEID-ANNOTATION`
- コードを修正しコミット
- コミットをスカッシュ `git rebase -i origin/master`
- コミットメッセージにfixesを追加
- push -f
- git pull-request -m "pull request title"

<lint check>
<compile check>
<coverage check>
<document check>
<no wip>

リリース準備
- リリースブランチをmasterから作成 `git checkout -b release-VERSION origin/master`
- version番号をbump `make bumpversion VERSION`

merge作業
- ターゲットのリリースブランチをチェックアウト `git checkout release-VERSION`
- パッチを適応 `git am -3 PULL-REQUEST-URL`
- コミットのAuthorとEmailを取得する
- 必要な修正を加える (必要であればスカッシュ) 問題点の修正、不要なスペースの削除、CHANGELOGの更新、テストの追加
- コミットメッセージにCloses #PULLID を追加
- コミットのAuthorとEmailを書き換える
- コミットをpush
- git-pr-release-likeでpullreqを作成 (コミットログに各commitのチェックボックスとユーザを加える)

<deploy application>
<deploy documentation>
<manual test> 動作確認がおわったらチェックボックスをonにする
<unittest>
<system test>
<aging test>
<qa test>
<performance test>
リ
oリース作業

- masterをチェックアウト `git checkout -b master origin/master`
- プルリクエストのチェックボックスがすべて付いているか確認
- パッチを適応 `git am -3 PULL-REQUEST-URL`
- empty commitで"Release version VERSION"を追加 `git commit -m "Release VERSION" --allow-empty`
- master migration and deploy
- タグを打つ `git tag VERSION && git push`

ステーブリング作業(リリース後しばらく問題が発生しなかった場合もしくはマイグレーションがある場合の作業)

- stableをチェックアウト `git checkout -b stable origin/stable`
- masterのcommitをpull `git pull origin master`
- git push
- stable deploy


fate issue create
fate issue fix
fate release create VERSION
fate release merge
