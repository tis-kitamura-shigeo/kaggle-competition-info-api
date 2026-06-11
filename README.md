# Kaggle Competition Info API

Kaggleコンペティション情報取得用REST APIサーバーです。

Kaggleのコンペティション情報（一覧・詳細）を取得するシンプルなAPIを提供します。

## 概要

FastAPI を用いて以下のエンドポイントを提供します。

- `GET /health`
  - サービスのヘルスチェック
- `GET /competitions`
  - コンペティション一覧を取得
- `GET /competitions/{competition_name}`
  - 指定コンペティションの詳細（および関連ページ）を取得

バックエンドでは `kagglesdk` のクライアントを利用して Kaggle API と通信します。

## 動作確認

- Python 3.12
- uv 0.11.6

## 環境構築

### 依存関係のインストール
```
uv sync
```

## 環境変数の設定
Kaggleの公式サイトから、APIトークンを発行します。

https://www.kaggle.com/settings/api

```
cp .env.sample .env
```

`.env` を編集し、発行したAPIトークンを設定します。
```
KAGGLE_API_TOKEN=your_kaggle_api_token_here
```

## 実行方法

```bash
uv run python main.py
```

または

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Dockerコンテナでの実行
```bash
docker build -t kaggle-competition-info-api .
docker run -e KAGGLE_API_TOKEN=YOUR_KAGGLE_API_TOKEN -p 8080:8080 kaggle-competition-info-api
```

## 動作確認

ヘルスチェック:

```bash
curl http://localhost:8000/health
```

コンペ一覧:

```bash
curl http://localhost:8000/competitions
```

特定コンペ詳細:

```bash
curl http://localhost:8000/competitions/titanic
```
