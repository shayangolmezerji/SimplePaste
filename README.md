# 🔐 SimplePaste: Private & Ephemeral Pastebin

This project is a minimalist, secure **Pastebin service** built with **Flask** and **Redis**. It's designed for sharing sensitive code or text quickly with a crucial feature: **automatic expiration**.

It demonstrates a robust, production-ready backend structure, utilizing Redis's powerful time-to-live (`TTL`) features for data management and a clean App Factory pattern for security and scalability.

-----

### ✨ Core Features

  * **Fast Ephemeral Storage:** Uses **Redis** as a blazing-fast in-memory database.
  * **Automatic Deletion:** Pastes are automatically removed by Redis after their set expiry time.
  * **Private Sharing:** Option to create a **token-gated URL** for private access.
  * **Production Ready:** Built with the **Flask App Factory** pattern, secure environment variables (`.env`), and designed for deployment with **Gunicorn**.
  * **Clean Architecture:** Simple three-file structure (`app.py`, `index.html`, `view.html`).

-----

### 🚀 Getting Started

You'll need **Python 3** and a running **Redis server** for this to work.

#### 1\. Grab the code

```bash
git clone https://github.com/shayangolmezerji/SimplePaste.git
cd simple-pastebin
```

#### 2\. Set up your environment

Use a virtual environment and install the required libraries.

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### 3\. Configure Secrets

Create a file named **`.env`** in the project root to securely manage your configurations:

```bash
# .env
SECRET_KEY="YOUR_SUPER_SECURE_RANDOM_KEY"
REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_DB="0"
```

#### 4\. Run the App

For development or production, use Gunicorn to start the server:

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

Access the application at `http://localhost:8000/`.

-----

### 💡 How to Use

1.  **Paste Content:** Enter your code or text.
2.  **Set Expiry:** Choose the duration (in minutes) after which the paste should be deleted.
3.  **Choose Privacy:** Check the **'Private?'** box to generate a unique, tokenized URL, ensuring only those with the full link can view it.

-----

### 📜 License

This project is licensed under the [Attribution-NonCommercial 4.0 International Public License](LICENSE.md).

### 👨‍💻 Author

Made with ❤️ by [Shayan Golmezerji](https://github.com/shayangolmezerji)
