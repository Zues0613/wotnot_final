# WotNot: The AI-Powered WhatsApp Marketing Automation Platform 🚀

**Author**: [Darshitha Marapareddy](https://github.com/Darshitha-03)

WotNot is a full-featured platform designed to revolutionize WhatsApp marketing through intelligent automation and AI-powered content creation. It empowers businesses to connect with their customers on a massive scale, moving beyond simple bulk messaging to create truly engaging experiences.  

With a sleek, fully responsive interface and powerful analytics, **WotNot is the ultimate tool for modern marketing.**

---

## 📋 Table of Contents
- [Why WotNot?](#-why-wotnot)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [About the Creator](#-about-the-creator)
- [License](#-license)

---

## 🔥 Why WotNot?
In a world saturated with digital noise, **direct communication is paramount**.  
WotNot transforms your WhatsApp into a dynamic tool for marketing and customer engagement.  

✔️ Move beyond manual, time-consuming messaging.  
✔️ Embrace intelligent, automated campaigns that capture attention and drive conversions.  

### Highlights:
- **Automate at Scale** – Schedule and send personalized bulk messages, order confirmations, and promotional campaigns.
- **AI-Powered Creativity** – Integrated with **Google Gemini AI** to craft compelling, high-impact message templates in seconds.
- **Seamless Cross-Device Experience** – Fully responsive UI for desktop, tablet, and mobile.
- **Data-Driven Decisions** – Track delivery, read rates, and engagement with an advanced analytics dashboard.

---

## ✨ Key Features
- 🤖 **Gemini-Powered Template Writer** – Instantly generate creative and effective marketing copy.  
- 📱 **Fully Responsive Interface** – Beautifully designed, mobile-friendly, and intuitive.  
- 📈 **Comprehensive Analytics** – Crystal-clear insights into campaign performance.  
- 🔒 **Secure Authentication** – Built with FastAPI for robust login and signup security.  
- 💬 **Integrated AI Assistant** – A ChatGPT-like assistant to guide you within the app.  
- 📦 **Bulk & Scheduled Messaging** – Effortlessly send messages to thousands or schedule them for the best time.  

---

## 🛠️ Technology Stack
WotNot is built on a modern, scalable, and reliable stack:

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) – High-performance, asynchronous Python APIs  
- **Frontend**: [Vue.js 3](https://vuejs.org/) – Reactive, component-based UI  
- **Database**: PostgreSQL (recommended)  
- **AI Integration**: Google Gemini API  

---

## 🚀 Getting Started

Follow these steps to run WotNot locally.

### Prerequisites
- Python **3.8+**  
- Node.js **v16+** and npm/yarn  
- PostgreSQL  
- .env File at /backend containing secrets
```
DATABASE_URL=
TURNSTILE_SECRET_KEY=
YOUR_KEY_ID=
YOUR_KEY_SECRET=
GEMINI_API_KEY =
```
### Installation

#### Clone the repository
```bash
git clone https://github.com/Darshitha-03/wotnot.git
cd wotnot
````

#### Backend Setup (FastAPI)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload
```

#### Frontend Setup (Vue.js)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run serve
```

---

## ▶️ Usage

1. Start the **backend** server (FastAPI).
2. Start the **frontend** (Vue.js).
3. Open the app in your browser (default: `http://localhost:8080`).
4. Sign up / log in, connect your WhatsApp, and start building automated campaigns.

---

## 👩‍💻 About the Creator

Built with ❤️ by **Darshitha Marapareddy**.
A passionate developer focused on building **AI-powered automation tools** that simplify workflows and maximize impact.

🔗 [GitHub Profile](https://github.com/Darshitha-03)

---

## 📜 License

This project is licensed under the **MIT License**.
Feel free to fork, modify, and distribute with attribution.

---

🚀 **WotNot** – Elevating WhatsApp Marketing with AI and Automation.
