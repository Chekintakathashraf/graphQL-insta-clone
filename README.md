# graphQL-insta-clone

uv setup

# Instagram Clone - Django Project

This project is a simple **Instagram Clone** built using **Django** and managed with **uv** for package management.

## 🚀 Getting Started

### **1. Install uv (if not installed)**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### **2. Create a New Django Project**

```bash
mkdir instagram_clone
cd instagram_clone
uv init .
uv add django python-dotenv
uv run django-admin startproject instagram_clone .
```

### **3. Create a Django App**

```bash
uv run python manage.py startapp social
```

### **4. Set Up Environment Variables**

Create a `.env` file in the root directory and add the following:

```ini
DEBUG=True
SECRET_KEY="your-secret-key"
DATABASE_URL="sqlite:///db.sqlite3"
```

### **5. Apply Migrations**

```bash
uv run python manage.py migrate
```

### **6. Create a Superuser (Optional)**

```bash
uv run python manage.py createsuperuser
```

### **7. Run the Development Server**

```bash
uv run python manage.py runserver
```

Access the project at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

## 📂 Project Structure

```
instagram_clone/
│── manage.py          # Django project manager
│── instagram_clone/   # Project settings and configurations
│── social/            # Social app for Instagram features
│── .env               # Environment variables (ignored in Git)
│── .gitignore         # Ignore files like .env and __pycache__
│── pyproject.toml     # uv project dependencies
```

## 📜 `.gitignore`

Ensure `.env` and other unnecessary files are ignored:

```
.env
__pycache__/
*.pyc
*.pyo
db.sqlite3
venv/
.venv/
```

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variables
DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")


## ✅ Features

- User authentication
- Post creation and likes
- Comments
- Follow/unfollow users
- Responsive UI

## 📌 Notes

- This project uses `uv`, so **no need to activate a virtual environment**.
- Use `uv run <command>` for running Django commands.

## 🛠️ Contributing

1. Fork the repo
2. Create a new branch
3. Commit your changes
4. Submit a Pull Request

## 📝 License

This project is open-source and available under the **MIT License**.





