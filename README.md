# 🩺 MediBot — AI Medical Symptom Advisor

MediBot is a lightweight AI-powered medical symptom advisor built with Python and Streamlit. It helps users describe symptoms conversationally and receive educational guidance, possible causes, home-care suggestions, and recommendations on when to seek professional medical attention.

> ⚠️ Disclaimer: MediBot is designed for educational purposes only and should not replace professional medical advice, diagnosis, or treatment.

---

# ✨ Features

* 💬 ChatGPT-style medical symptom conversation UI
* 🧠 AI-powered responses using Groq + Llama 3.3
* 📊 Built-in feedback collection system
* 📈 Session analytics dashboard
* 📝 Interaction logging with JSON storage
* 🔍 Automated performance analysis script
* ⚡ Quick symptom suggestion buttons
* 🧹 Clear chat functionality
* 🎨 Clean Streamlit interface

---

# 🏗️ Project Structure

```bash
MediBot/
│
├── agent.py                # Main Streamlit medical chatbot
├── analyze.py              # Feedback analytics & reporting tool
├── feedback_log.json       # Stored user interactions & feedback
├── analysis_report.md      # Generated project analysis report
├── improvement_demo.md     # Improvement examples/documentation
├── README.md               # Project documentation
└── .env                    # Environment variables (not committed)
```

---

# ⚙️ Tech Stack

* Python 3.10+
* Streamlit
* Groq API
* OpenAI Python SDK
* JSON-based logging

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/hayakhan-ai/MediBot.git
cd MediBot
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install streamlit openai python-dotenv
```

---

# 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# ▶️ Running the Application

Start the Streamlit app:

```bash
streamlit run agent.py
```

The application will open in your browser automatically.

---

# 📊 Running Analytics

Analyze user feedback and chatbot performance:

```bash
python analyze.py
```

This script provides:

* Total interactions
* Positive vs negative feedback
* Satisfaction rate
* Top failed symptom queries
* Reviewable failed interactions

---

# 🧠 How MediBot Works

1. User enters symptoms in chat
2. Prompt is sent to Groq-hosted Llama model
3. AI generates:

   * Empathy response
   * Possible causes
   * OTC/home-care suggestions
   * Doctor warning signs
4. User can provide feedback
5. Interactions are stored in `feedback_log.json`
6. `analyze.py` evaluates overall chatbot quality

---

# 📸 Core Functionalities

## Medical Guidance

MediBot provides:

* Symptom understanding
* Basic OTC suggestions
* Educational explanations
* Medical escalation warnings

## Feedback Loop

Users can rate responses:

* 👍 Good
* 👎 Bad
* Skip

This enables future improvement and analysis.

---

# 🔒 Security Notes

* Never hardcode API keys
* Always use `.env`
* Add `.env` to `.gitignore`
* Regenerate exposed API keys immediately

Recommended `.gitignore`:

```gitignore
.env
__pycache__/
venv/
```

---

# ⚠️ Limitations

MediBot:

* Does NOT provide real medical diagnosis
* Should NOT be used in emergencies
* Can produce incorrect AI-generated responses
* Requires human medical verification

---

# 🔮 Future Improvements

Potential enhancements:

* Multi-language support
* Medical knowledge base integration
* User authentication
* Persistent chat history
* RAG-based medical retrieval system
* PDF medical report generation
* Voice input support
* Docker deployment
* Advanced analytics dashboard

---

# 👩‍💻 Author

**Haya M Khan**

* GitHub: [https://github.com/hayakhan-ai](https://github.com/hayakhan-ai)
* LinkedIn: [https://linkedin.com/in/haya-m-khan](https://linkedin.com/in/haya-m-khan)

---

# 📄 License

This project is open-source and available under the MIT License.

---

# ⭐ Support

If you found this project useful:

* Star the repository
* Fork the project
* Contribute improvements
* Share feedback

---

# 🩺 Educational Use Only

MediBot is intended for:

* AI learning projects
* Healthcare chatbot experimentation
* NLP demonstrations
* Educational software engineering portfolios

It is NOT approved for clinical or diagnostic use.
