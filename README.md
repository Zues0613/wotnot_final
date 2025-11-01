# WotNot: The AI-Powered WhatsApp Marketing Automation Platform 🚀

**Authors**: [Darshitha Marapareddy](https://github.com/Darshitha-03) & [**Vishal D**](https://github.com/zues0613)

WotNot is a comprehensive, production-ready WhatsApp marketing automation platform that revolutionizes business communication through intelligent automation and AI-powered content creation. It empowers businesses to connect with their customers at scale, moving beyond simple bulk messaging to create truly engaging, personalized experiences.

With a modern Vue.js frontend, robust FastAPI backend, and advanced AI integration, **WotNot is the ultimate solution for modern WhatsApp marketing automation.**

---

## 📋 Table of Contents
- [Why WotNot?](#-why-wotnot)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Status](#-project-status)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [About the Authors](#-about-the-authors)
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

### 🤖 AI-Powered Content Generation
- **Google Gemini AI Integration** – Generate compelling message templates instantly
- **OpenAI (OpenRouter) Support** – Advanced AI capabilities for content creation
- **AI Assistant** – ChatGPT-like interface for real-time assistance
- **Customizable Tone & Length** – Tailor messages to your brand voice

### 📱 WhatsApp Business Integration
- **Template Management** – Create, submit, and manage WhatsApp message templates
- **Bulk Messaging** – Send messages to thousands of contacts with rate limiting
- **Scheduled Broadcasting** – Plan and automate message campaigns
- **Real-time Chat** – Live WhatsApp conversation management
- **Media Support** – Upload and share images, documents, and media

### 📊 Advanced Analytics & Reporting
- **Delivery Tracking** – Monitor sent, delivered, read, and replied status
- **Performance Analytics** – Detailed insights into campaign effectiveness
- **Cost Analytics** – Track spending and ROI with visual dashboards
- **Error Reporting** – Comprehensive error tracking and resolution

### 🔗 E-commerce Integration
- **WooCommerce Integration** – Automated order confirmations and notifications
- **Product-based Messaging** – Targeted campaigns based on product purchases
- **Webhook Support** – Real-time event processing
- **Store Management** – Connect and manage multiple WooCommerce stores

### 👥 Contact Management
- **Bulk Import/Export** – CSV-based contact management
- **Tag System** – Organize contacts with custom tags
- **Duplicate Detection** – Smart contact deduplication
- **Search & Filter** – Advanced contact filtering capabilities

### 🔒 Security & Authentication
- **JWT Authentication** – Secure token-based authentication
- **OAuth2 Integration** – WhatsApp Business API integration
- **API Key Management** – Secure API access for integrations
- **Data Protection** – Comprehensive security measures  

---

## 🛠️ Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12.3) – High-performance, asynchronous APIs
- **Database**: PostgreSQL with SQLAlchemy (Async) – Robust data persistence
- **Task Queue**: Dramatiq with Redis – Background job processing
- **Authentication**: JWT tokens with OAuth2 – Secure user management
- **AI Integration**: Google Gemini API + OpenAI (OpenRouter) – Advanced AI capabilities
- **Background Processing**: APScheduler – Scheduled task management

### Frontend
- **Framework**: [Vue.js 3](https://vuejs.org/) – Modern reactive UI framework
- **UI Library**: Element Plus + Tailwind CSS – Beautiful, responsive components
- **State Management**: Vuex (implicit) – Application state management
- **HTTP Client**: Axios – API communication
- **Charts**: Chart.js with Vue-Chart-3 – Data visualization

### Infrastructure
- **Database**: PostgreSQL – Primary data storage
- **Cache/Queue**: Redis – Caching and message queuing
- **File Storage**: Local + WhatsApp Media API – Media management
- **Deployment**: Heroku-ready (Procfile included) – Easy deployment  

---

## 📊 Project Status

**Current Status**: ✅ **PRODUCTION READY**

WotNot is a fully functional, production-ready WhatsApp marketing automation platform with comprehensive features:

- ✅ **Complete Feature Set** - All core functionality implemented and working
- ✅ **Modern Architecture** - Built with current best practices and technologies  
- ✅ **Scalable Design** - Handles growing user bases and message volumes
- ✅ **AI Integration** - Advanced AI capabilities for content generation
- ✅ **Real-time Features** - Live chat, analytics, and message tracking
- ✅ **E-commerce Ready** - WooCommerce integration for automated workflows

### Recent Updates
- Enhanced AI integration with multiple providers
- Improved real-time chat functionality
- Advanced analytics and reporting
- WooCommerce automation features
- Comprehensive error handling and logging
- Performance optimizations

---

## 🚀 Getting Started

Follow these steps to run WotNot locally.

### Prerequisites
- Python **3.12.3** (recommended)
- Node.js **v16+** and npm/yarn  
- PostgreSQL database
- Redis server
- WhatsApp Business API credentials
- .env File at /backend containing secrets

### Environment Variables
Create a `.env` file in the `/backend` directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/wotnot_db

# Redis
REDIS_URL=redis://localhost:6379

# AI Integration
GEMINI_API_KEY=your_gemini_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# WhatsApp Business API
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
REDIRECT_URI=http://localhost:8081/broadcast/broadcast2

# Optional
TURNSTILE_SECRET_KEY=your_turnstile_key
```
### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/Darshitha-03/wotnot.git
cd wotnot
```

#### 2. Backend Setup (FastAPI)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python migrate_db.py --action create

# 🚀 Start ALL services with one command (Recommended)
python start_all.py

# OR start services individually:
# Start Redis (required for background tasks)
python start_redis.py

# In a separate terminal, start Dramatiq worker
python start_dramatiq.py

# In another terminal, start FastAPI server
python start_backend.py
```

**🎯 Quick Start (One Command):**
```bash
# This starts Redis, Dramatiq, and FastAPI automatically
python start_all.py

# On Windows, you can also use:
start_all.bat
```

#### 3. Frontend Setup (Vue.js)

```bash
# Navigate to frontend/app
cd frontend/app

# Install dependencies
npm install

# Run development server
npm run serve
```

---

## ▶️ Usage

### Quick Start (Recommended)
1. **Start all backend services** with one command:
   ```bash
   cd backend
   python start_all.py
   ```
   This automatically starts Redis, Dramatiq worker, and FastAPI server.

2. **Start the frontend** (Vue.js) on `http://localhost:8080`

3. **Open the app** in your browser and sign up/log in

4. **Connect your WhatsApp Business Account**

5. **Start creating templates and sending automated campaigns!**

### Manual Start (Alternative)
If you prefer to start services individually:
1. Start Redis: `python start_redis.py`
2. Start Dramatiq: `python start_dramatiq.py` 
3. Start Backend: `python start_backend.py`
4. Start Frontend: `npm run serve`

### Quick Start Guide
1. **Register** a new account
2. **Connect WhatsApp** using OAuth2 flow
3. **Create templates** using AI-powered generator
4. **Import contacts** via CSV or manual entry
5. **Send broadcasts** immediately or schedule them
6. **Monitor analytics** and track performance

---

## 📚 API Documentation

WotNot provides a comprehensive REST API built with FastAPI:

- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Key API Endpoints
- **Authentication**: `/login`, `/register`, `/subscribe_customer`
- **Broadcasting**: `/send-template-message/`, `/broadcast`
- **Templates**: `/template`, `/create-template`
- **Contacts**: `/contacts/`, `/contacts/bulk_import/`
- **Analytics**: `/get-analytics`, `/broadcast-report/{id}`
- **Integration**: `/test-woocommerce`, `/woo_products`

---

## 🚀 Deployment

### Heroku Deployment (Recommended)
```bash
# Backend deployment
git subtree push --prefix=backend heroku main

# Frontend deployment (static hosting)
cd frontend/app
npm run build
# Deploy the 'dist' folder to any static host
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Environment Setup
- Set up PostgreSQL database
- Configure Redis instance
- Set all required environment variables
- Configure WhatsApp Business API webhooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend components
- Write tests for new features
- Update documentation as needed

---

## 👥 About the Authors

Built with ❤️ by **Darshitha Marapareddy** and **Vishal D**.

**Darshitha Marapareddy** - A passionate developer focused on building **AI-powered automation tools** that simplify workflows and maximize impact.

**Vishal D** - A dedicated Full-Stack Developer, AI & Cloud Enthusiast, and CSE Student with expertise in scalable systems and modern web technologies.

🔗 [Darshitha's GitHub Profile](https://github.com/Darshitha-03)  
🔗 [Vishal's GitHub Profile](https://github.com/zues0613)

---

## 📜 License

This project is licensed under the **MIT License**.
Feel free to fork, modify, and distribute with attribution.

---

## 🎉 Project Highlights

WotNot represents a significant achievement in WhatsApp marketing automation:

- **🏆 Production Ready** - Fully functional platform ready for real-world deployment
- **🤖 AI-Powered** - Advanced AI integration for intelligent content generation
- **📊 Data-Driven** - Comprehensive analytics and reporting capabilities
- **🔗 E-commerce Ready** - Seamless integration with WooCommerce and other platforms
- **⚡ High Performance** - Optimized for speed and scalability
- **🔒 Enterprise Security** - Robust authentication and data protection

## 📈 What's Next

- **Multi-tenancy Support** - Support for multiple organizations
- **Mobile App** - Native mobile application development
- **Advanced AI** - Machine learning for message optimization
- **More Integrations** - Shopify, Magento, and other e-commerce platforms
- **API Marketplace** - Third-party integration ecosystem

---

🚀 **WotNot** – The Future of WhatsApp Marketing Automation is Here!

*Built with modern technologies, powered by AI, and designed for scale.*
