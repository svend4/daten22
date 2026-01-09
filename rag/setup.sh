#!/bin/bash
# Setup script for MBTI RAG System

echo "🧠 MBTI RAG System - Setup"
echo "=========================="
echo ""

# Check Python version
echo "🔍 Проверка Python..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python версия: $python_version"

# Create virtual environment
echo ""
echo "📦 Создание виртуального окружения..."
python3 -m venv venv
echo "   ✓ Виртуальное окружение создано"

# Activate virtual environment
echo ""
echo "🔧 Активация окружения..."
source venv/bin/activate
echo "   ✓ Окружение активировано"

# Install dependencies
echo ""
echo "📥 Установка зависимостей..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "   ✓ Зависимости установлены"

# Copy .env if doesn't exist
echo ""
echo "⚙️  Настройка конфигурации..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   ✓ Создан файл .env (измените при необходимости)"
else
    echo "   ✓ Файл .env уже существует"
fi

# Create data directory
echo ""
echo "📁 Создание директорий..."
mkdir -p data/chroma_db
echo "   ✓ Директории созданы"

# Run indexer
echo ""
echo "🔨 Запуск индексации документов..."
python scripts/indexer.py

# Check if indexing was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Установка завершена успешно!"
    echo ""
    echo "🚀 Запуск системы:"
    echo "   CLI:  python cli.py"
    echo "   Web:  streamlit run app/streamlit_app.py"
    echo ""
    echo "📚 Документация: cat README.md"
else
    echo ""
    echo "❌ Ошибка при индексации"
    echo "   Проверьте наличие документов в ../docs/ и ../types/"
fi
