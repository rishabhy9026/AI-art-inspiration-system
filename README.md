# 🤖 Aria AI – Smart Chatbot & Vision Assistant

A real-time AI chatbot and vision analysis system built using **Flask**, **Groq API**, and **LLMs** for intelligent conversations and image understanding.
<img width="1806" height="905" alt="Screenshot 2026-04-21 225143" src="https://github.com/user-attachments/assets/98a3b03d-60ff-46e6-9abf-f09121766566" />
<img width="1903" height="977" alt="Screenshot 2026-04-21 005539" src="https://github.com/user-attachments/assets/ed2dea94-21a8-4827-bba0-8f9d7c5b6e4b" />
<img width="1901" height="964" alt="Screenshot 2026-04-21 225246" src="https://github.com/user-attachments/assets/7611960d-db54-4caa-9863-412920c1a8a8" />


## 📌 Features

- 💬 AI-powered chatbot (Aria)
- 🤖 Groq API integration (Mixtral + LLaMA models)
- 🧠 Context-aware intelligent responses
- 🖼️ Image analysis using vision model
- 🔐 Session-based login system
- 🌐 Flask backend with REST APIs
- ⚡ Fast response time with optimized inference
- 🔄 CORS enabled for frontend-backend communication

---

## ⚙️ System Requirements

- Python 3.8+
- Internet connection (for Groq API)
- Modern web browser

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rishabh9026/aria-ai-project.git
cd aria-ai-project

2. Install Dependencies\

pip install -r requirements.txt
3. Setup Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key

🚀 Usage
1. Start the Flask Application
python app.py
2. Open the Web Interface

Visit: http://localhost:5000

🔌 API Endpoints

Endpoint	Description
/chat	Send message to AI chatbot
/vision	Analyze image using AI
/login	User login
/logout	End session
Example:

curl -X POST http://localhost:5000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Hello Aria"}'
🛠️ Configuration
Groq API Key: Set GROQ_API_KEY in .env
Model Used:
mixtral-8x7b-32768 (chat)
llama-vision (image analysis)
Session Secret: Controlled via SECRET_KEY
⚡ Performance Considerations
⚡ Fast inference using Groq acceleration
🚀 Lightweight Flask backend
📉 Low latency for chat responses

🔒 Security

Requires secure storage of API keys
Uses session-based authentication
Do NOT expose .env file publicly

📂 Project Structure

aria-ai-project/
│── app.py
│── requirements.txt
│── .env
│
├── static/
│   ├── images/
│   ├── index.html
│   ├── login.html
│
└── templates/

🤝 Contributing

We welcome contributions!

Fork the repo
Create a branch (git checkout -b feature-name)
Commit your changes
Push to your branch (git push origin feature-name)
Open a Pull Request 🚀
📄 License

This project is licensed under the MIT License.

📝 Additional Notes

Replace placeholder screenshots with actual images
Keep API keys secure
Add deployment (Render / AWS / Vercel) for live demo

---


- or add **badges + demo + architecture diagram** 🚀
---
