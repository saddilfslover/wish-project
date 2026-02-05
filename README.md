# 🎯 Доска Желаний (Wishlist App)

Telegram Mini App для создания списка желаний.

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/saddilfslover/wish-project.git
cd wish-project

cd backend
pip install -r requirements.txt
# Настройте .env файл (скопируйте из .env.example)
uvicorn main:app --reload --port 8000

cd frontend
npm install
npm run dev
