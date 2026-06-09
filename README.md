Markdown
# 🤖 Makobot - Local AI Chatbot

Makobot is a fully functional, locally hosted Full-Stack AI Chatbot built with Python. It leverages local large language models (LLMs) to ensure 100% data privacy and zero API costs, while seamlessly logging usage analytics to the cloud.

## ✨ Features
* **Local AI Processing:** Powered by the `Gemma 2` model via Ollama, ensuring fast responses and complete privacy. No data is sent to OpenAI or Google for inference.
* **Interactive UI:** Built with Streamlit for a smooth, real-time chat experience with typewriter streaming effects.
* **Dynamic Personas:** Users can select different AI personalities (e.g., Teacher, Programmer, Musician, or custom humorous characters) via a sidebar. The bot dynamically adapts its system prompts and avatars.
* **Cloud Logging:** Asynchronously saves chat metadata (prompts, responses, generation time, and active persona) to a Firebase Firestore NoSQL database for analytics.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend/AI:** Ollama, Gemma 2 (9B)
* **Database:** Firebase / Firestore
* **Language:** Python

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/Makobot.git](https://github.com/YOUR-USERNAME/Makobot.git)
   cd Makobot
Install dependencies:

Bash
pip install -r requirements.txt
Install and run Ollama:

Download Ollama from ollama.com

Pull the Gemma 2 model:

Bash
ollama pull gemma2
Firebase Setup:

Create a Firebase project and a Firestore database.

Generate a private key JSON file from Project Settings > Service Accounts.

Rename the file to firebase_key.json and place it in the root directory. (Note: This file is gitignored for security).

Start the app:

Bash
streamlit run app.py

---

