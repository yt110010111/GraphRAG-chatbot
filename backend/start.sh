#!/bin/bash

echo "Starting Ollama service..."
# 啟動 Ollama 服務在背景
ollama serve &

echo "Waiting for Ollama to start..."
# 等待 Ollama 服務啟動
sleep 10

echo "Pulling Ollama model..."
# 下載模型（在背景執行，避免阻塞）
ollama pull llama3 &

echo "Running database migrations..."
# 執行資料庫遷移
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Starting Django server..."
# 啟動 Django 服務
python manage.py runserver 0.0.0.0:8001