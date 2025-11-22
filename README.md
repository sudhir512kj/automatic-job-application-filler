# 🤖 Auto Form Filling GenAI Agent

A smart application that automatically fills Google Forms using your resume data with AI-powered field mapping.

## ✨ Features

- 📄 **Resume Parsing**: Supports PDF, DOCX, and TXT formats
- 🧠 **AI-Powered**: Uses OpenRouter and Llama Cloud APIs for intelligent data extraction
- 🎯 **Smart Form Filling**: Automatically maps resume data to Google Form fields
- 🚀 **Direct Submission**: Submits forms without browser automation
- 💻 **User-Friendly**: Clean React interface with drag-and-drop upload

## 🛠️ Tech Stack

**Backend**: FastAPI, OpenRouter API, Llama Cloud API, Google Forms API  
**Frontend**: React 18, Axios, Bootstrap  
**AI Libraries**: LlamaIndex, OpenRouter LLM

## 🚀 Quick Start Guide

### Option 1: Docker (Recommended) 🐳

**📖 For detailed Docker setup, see [DOCKER_SETUP_GUIDE.md](DOCKER_SETUP_GUIDE.md)**

#### Prerequisites
- Docker and Docker Compose installed
- Git installed

#### Quick Steps
1. Clone the repository:
```bash
git clone <your-repo-url>
cd auto-form-filling-agent
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Add your API keys to `.env`:
```
OPENROUTER_API_KEY=your_openrouter_key_here
LLAMA_CLOUD_API_KEY=your_llama_cloud_key_here
```

4. Run with Docker:
```bash
docker-compose up --build
```

✅ **Application running at:**
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

> 💡 **Need help with Docker?** Check the comprehensive [Docker Setup Guide](DOCKER_SETUP_GUIDE.md) for troubleshooting, development workflow, and advanced configurations.

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd auto-form-filling-agent
```

### Step 2: Get API Keys (Required)

#### OpenRouter API Key (Free)
1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Go to "Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-...`)

#### Llama Cloud API Key (Free)
1. Go to [Llama Cloud](https://cloud.llamaindex.ai/)
2. Sign up for a free account
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `llx-...`)

### Step 3: Setup Backend

#### Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Or on Windows
venv\Scripts\activate
```

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the `backend` folder:
```bash
cd backend
touch .env
```

Add your API keys to `.env`:
```
OPENROUTER_API_KEY=your_openrouter_key_here
LLAMA_CLOUD_API_KEY=your_llama_cloud_key_here
```

#### Start Backend Server
```bash
python main.py
```
✅ Backend running at: `http://localhost:8000`

### Step 4: Setup Frontend

#### Install Dependencies
```bash
# Open new terminal
cd frontend
npm install
```

#### Start Frontend
```bash
npm start
```
✅ Frontend running at: `http://localhost:3000`

### Option 3: AWS EC2 Deployment (Production)

#### Prerequisites
- AWS CLI installed and configured
- AWS account with appropriate permissions

#### Steps
1. Clone and setup:
```bash
git clone <your-repo-url>
cd auto-form-filling-agent
```

2. Deploy to AWS EC2:
```bash
# Make script executable
chmod +x aws/deploy-fullstack-ec2.sh

# Deploy full stack
./aws/deploy-fullstack-ec2.sh
```

3. Add API keys:
```bash
# SSH into instance (use IP from deploy output)
ssh -i ~/.ssh/auto-form-filler-key.pem ubuntu@[EC2-IP]

# Add your API keys
echo "OPENROUTER_API_KEY=your_key_here" >> auto-form-filling-agent/.env
echo "LLAMA_CLOUD_API_KEY=your_key_here" >> auto-form-filling-agent/.env

# Restart containers
cd auto-form-filling-agent
sudo docker-compose restart
```

✅ **Production deployment complete!**

See `aws/README.md` for detailed deployment guide.

## 🎯 How to Use

### 1. Prepare Your Resume
- Save your resume as PDF, DOCX, or TXT
- Include: Name, Email, Phone, Skills, Education, Work Experience

### 2. Get Google Form URL
- Open any Google Form
- Copy the URL (should contain `docs.google.com/forms`)

### 3. Fill the Form
1. Open `http://localhost:3000`
2. Upload your resume file
3. Paste the Google Form URL
4. Click "Submit Form Directly"
5. ✅ Form submitted automatically!

## 📁 Project Structure

```
auto-form-filling-agent/
├── backend/
│   ├── services/
│   │   ├── resume_parser.py         # AI resume parsing
│   │   └── google_forms_service.py  # Form submission
│   ├── main.py                      # FastAPI server
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Development container
│   ├── Dockerfile.prod              # Production container
│   └── .env                         # API keys (create this)
├── frontend/
│   ├── src/
│   │   ├── components/              # React components
│   │   └── services/                # API calls
│   ├── package.json                 # Node dependencies
│   ├── Dockerfile                   # Frontend container
│   └── public/
├── aws/
│   ├── deploy-fullstack-ec2.sh      # AWS EC2 deployment script
│   ├── fullstack-user-data.sh       # EC2 initialization script
│   ├── cleanup-all-resources.sh     # Resource cleanup script
│   └── README.md                    # AWS deployment guide
├── docker-compose.yml               # Local development
├── .env.example                     # Environment template
├── DOCKER_SETUP_GUIDE.md            # 🐳 Comprehensive Docker guide
└── README.md
```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/parse-resume` | POST | Extract data from resume |
| `/api/analyze-form` | POST | Analyze Google Form structure |
| `/api/fill-form` | POST | Fill and submit form |
| `/api/health` | GET | Health check |
| `/api/hello` | GET | Test endpoint |

## 🐛 Troubleshooting

### Backend Issues

**Error: "Module not found"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r backend/requirements.txt
```

**Error: "API key not found"**
- Check `.env` file exists in `backend/` folder
- Verify API keys are correct (no extra spaces)
- Restart backend server after adding keys

### Frontend Issues

**Error: "npm command not found"**
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Restart terminal after installation

**Error: "Connection refused"**
- Make sure backend is running on port 8000
- Check `http://localhost:8000/api/health`

### Form Submission Issues

**Error: "Invalid form URL"**
- Use Google Forms URLs only
- URL should contain `docs.google.com/forms`
- Try with a simple test form first

## 🎓 For Students & Beginners

### Learning Resources
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
- **React**: [reactjs.org](https://reactjs.org/)
- **Python Virtual Environments**: [docs.python.org](https://docs.python.org/3/tutorial/venv.html)

### Common Commands

#### Docker Commands
```bash
# Start application
docker-compose up

# Start in background
docker-compose up -d

# Rebuild containers
docker-compose up --build

# Stop application
docker-compose down

# View logs
docker-compose logs
```

#### Manual Setup Commands
```bash
# Check Python version
python --version

# Check Node version
node --version

# Install Python package
pip install package_name

# Install Node package
npm install package_name
```

### Project Customization
- **Add new resume fields**: Edit `resume_parser.py`
- **Change AI models**: Modify `config.py`
- **Update UI**: Edit React components in `frontend/src/components/`
- **Add new endpoints**: Add routes in `main.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Create Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Need Help?

- **Docker Issues**: Check [DOCKER_SETUP_GUIDE.md](DOCKER_SETUP_GUIDE.md)
- **GitHub Issues**: Create an issue with logs and error messages
- **Questions**: Check existing issues first
- **Documentation**: Read this README and Docker guide carefully

---

**Happy Coding! 🚀**

*Made with ❤️ for students and developers*