#  リポジトリ名

## リポジトリの概要

リポジトリの目的と主な機能についての簡潔な説明。

### 例

このリポジトリは、Pythonプロジェクトのテンプレートです。プロジェクトの構造を画一化することで、可読性を向上させ、開発効率を高めることを目的としています。
Pythonを主として使用するプロジェクトの場合は、必ずこのテンプレートからプロジェクトを開始してください。

## 導入方法

- プロジェクトをローカルで実行するための手順
  - 必要なソフトウェアやツールのインストール方法
  - 依存関係のインストール方法
  - 環境設定ファイルの設定方法

### 例

1. リポジトリをクローン

    ```bash
    git clone <URL>
    ```

2. 依存関係をインストール

    ```bash
    pip install -e .
    ```

3. プロジェクト名を変更

    ```bash
    make rename-project

    # Renaming project
    # Enter new project name (kebab-case):
    # > new-project-name
    ```

4. (開発者向け) 開発用の依存関係をインストール

    ```bash
    pip install -e .[coding]
    ```

5. (開発者向け, VSCode / Cursor) RuffのVSCode拡張機能をインストール

    - [Ruff extension](https://marketplace.cursorapi.com/items?itemName=charliermarsh.ruff)をインストール
    - IDEの`settings.json` に以下を追加（このプロジェクトの`.vscode/settings.json`にも記載済み）

    ```json
    "[python]": {
      "editor.formatOnType": true,
      "editor.formatOnSave": true,
      "ruff.lint.enable": true,
      "ruff.lint.args": [
        "--config=pyproject.toml"
      ],
      "editor.codeActionsOnSave": {
        "source.fixAll": "explicit",
        "source.organizeImports": "explicit"
      },
      "ruff.importStrategy": "fromEnvironment"
    }
    ```

## 使用方法

プロジェクトの実行方法やMakefileのコマンド、その他の使い方についての説明。

### 例

- コーディング用環境のセットアップ

```bash
make prepare-develop-environment
```

- テストの実行

```bash
pytest
```

- 依存ライブラリの追加

`pyproject.toml` に追加したいライブラリを記述してください。

```diff toml
# ここにdependencyを入力する
dependencies = [
+   "numpy==1.19.5",
]
```


## プロジェクト構造

主要なディレクトリとファイルの構造についての説明。

### 例

- `data/` : 学習データセットなど、データの格納場所
- `models/` : 学習済みモデルの格納場所
- `docker/` : Dockerfileや関連ファイルの格納場所
- `src/{project_name}` : ソースコード
- `tests/` : テストコード
- `assets/` : READMEに使用する画像や図、サンプルデータ等の格納場所
- `server/` : サーバーサイドのコード

## ドキュメント

プロジェクトのドキュメントについての説明。NotionのリンクやWikiのリンクを記載する。

## Optional: APIドキュメント

APIのエンドポイントとリクエスト/レスポンスの仕様についての説明。

## Optional: ライセンス

ライセンスについての説明。

