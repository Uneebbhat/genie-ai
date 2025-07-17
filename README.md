# 🤖 Genie AI — Gemini-Powered Desktop Chatbot

**Genie AI** is a desktop-based chatbot that enables natural language conversations using Google's **Gemini API**. The project features a modular architecture, combining a modern desktop GUI (built with **CustomTkinter**), a Python **Flask** backend, and optional **MongoDB** integration for persistent chat logs.

Developed for the **Open Source Software** course, Genie AI follows best practices for Git-based collaboration, including feature branches, pull requests, and strict merge controls.

---

## 🌟 Features

- 💬 Conversational AI interface powered by Gemini API
- 🖥️ Intuitive, responsive GUI using CustomTkinter
- 🔄 Real-time interaction via a Flask API backend
- 🧠 Clean separation of API keys and model settings through a configuration module
- 🗂️ Optional MongoDB integration for saving chat logs
- 🔐 Secure secrets management using `.env` files
- 🗝️ Forgot Password feature to securely reset user passwords 
- 🚀 Open-source workflow with GitHub PR-based collaboration

---

## 🛠️ Tech Stack

| Component     | Technology             |
| ------------- | ---------------------- |
| Frontend      | Python + CustomTkinter |
| Backend       | Flask                  |
| AI Engine     | Gemini API             |
| Configuration | python-dotenv          |
| Database      | MongoDB (PyMongo)      |
| Versioning    | Git + GitHub           |

---

## 📁 Project Structure

```
genie-ai/
│
├── frontend/
│   ├── main.py        # GUI entry point (CustomTkinter)
│   └── README.md      # Project documentation
│
├── backend/
│   ├── app.py         # Flask app and API endpoints
│   ├── .env           # API keys and secrets (excluded from Git)
│   ├── config/
│   │   ├── geminiConfig.py  # Gemini API config management
│   │   └── dbConnect.py     # MongoDB connection
│   └── services/
│       └── generativeContent.py # Gemini API interaction logic
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/genie-ai.git
cd genie-ai
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=your_mongodb_connection_string   # optional
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Uneebbhat/genie-ai.git
   cd genie-ai
   ```
2. **Install dependencies:**
   - For the frontend (GUI):
     ```bash
     pip install customtkinter
     ```
   - For the backend (Flask, PyMongo, python-dotenv):
     ```bash
     pip install flask pymongo python-dotenv
     ```

---

## 🚦 Usage

1. **Start the backend server:**
   ```bash
   cd backend
   python app.py
   ```
2. **Run the desktop GUI:**
   ```bash
   cd ../frontend
   python main.py
   ```
3. **Interact with Genie AI:**
   - Enter your queries in the GUI and receive responses powered by Gemini API.
   - Click **Forgot Password?** on the login screen to reset your password securely if needed.
   - (Optional) If MongoDB is configured, chat logs will be saved automatically.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork the repository** and create a new branch for your feature or bugfix.
2. **Make your changes** with clear, descriptive commit messages.
3. **Open a pull request** to the `release` branch. Please describe your changes and reference any related issues.
4. Ensure your code follows the project's style and passes any tests.

For major changes, please open an issue first to discuss what you would like to change.

---
