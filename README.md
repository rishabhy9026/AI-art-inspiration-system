<img width="1903" height="977" alt="Screenshot 2026-04-21 005539" src="https://github.com/user-attachments/assets/5ef82a71-49cf-4e58-ad06-5abac7133a1e" />🤖 Aria AI – Smart Chatbot & Vision Assistant

An intelligent AI-powered chatbot web application built with Flask, Groq API, and LLM models, capable of handling conversations and analyzing images using vision models.

<img width="1903" height="977" alt="Screenshot 2026-04-21 005539" src="https://github.com/user-attachments/assets/d09b7272-15aa-407e-9944-e1e27f3a8cf3" />


📌 Features
💬 AI Chatbot (Aria) with natural conversation abilities
🤖 Powered by Groq API (Mixtral + LLaMA models)
🧠 Context-aware responses using system prompts
🖼️ Image analysis using vision model
🔐 Basic login system (session-based)
🌐 Flask backend with REST API
⚡ Fast responses with optimized LLM inference
🔄 CORS enabled for frontend-backend communication
⚙️ Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
AI Models: Groq API (Mixtral-8x7b, LLaMA Vision)
Environment Management: python-dotenv
Other: REST APIs, Session handling
🛠️ System Requirements
Python 3.8+
Internet connection (for Groq API)
Modern web browser
🛠️ Installation
1. Clone the Repository
git clone https://github.com/yourusername/aria-ai-project.git
cd aria-ai-project
2. Install Dependencies
pip install -r requirements.txt
3. Setup Environment Variables

Create a .env file in the root directory:

GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
🚀 Usage
Start the Application
python app.py
Open in Browser
http://localhost:5000
🔌 API Endpoints
Endpoint	Description
/chat	Send message to AI chatbot
/vision	Analyze image using AI
/login	User login
/logout	End session
Example Request
curl -X POST http://localhost:5000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Hello Aria"}'
🛠️ Configuration
Model Used:
mixtral-8x7b-32768 (chat)
llama-vision (image analysis)

API URL:

https://api.groq.com/openai/v1/chat/completions
Session Secret:
Controlled via SECRET_KEY
⚡ Performance
🚀 Fast inference using Groq hardware acceleration
⚡ Lightweight Flask backend
📉 Minimal latency for chat responses
🔒 Security
🔐 Session-based authentication
🔑 API keys stored securely in .env
⚠️ Do NOT expose your Groq API key publicly
📂 Project Structure
Aria-AI-project/
│── app.py
│── .env
│── requirements.txt
│
├── Static/
│   ├── index.html
│   ├── login.html
│
└── venv/ (ignored)
🤝 Contributing

Contributions are welcome!

Fork the repository
Create a new branch
git checkout -b feature-name
Commit your changes
Push to GitHub
git push origin feature-name
Open a Pull Request 🚀
📄 License

This project is licensed under the MIT License.

📬 Contact
GitHub: https://github.com/yourusername
Email: your@email.com
📝 Notes
Add real screenshots for better presentation
Remove venv/ before pushing to GitHub (use .gitignore)
Keep API keys secure
