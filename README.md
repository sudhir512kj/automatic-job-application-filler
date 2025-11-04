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

### Prerequisites
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
│   │   ├── resume_parser.py      # AI resume parsing
│   │   ├── google_forms_service.py # Form submission
│   │   └── form_analyzer.py      # Form analysis
│   ├── main.py                   # FastAPI server
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # API keys (create this)
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   └── services/             # API calls
│   ├── package.json              # Node dependencies
│   └── public/
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
```bash
# Check Python version
python --version

# Check Node version
node --version

# Install Python package
pip install package_name

# Install Node package
npm install package_name

# See running processes
# Mac/Linux: ps aux | grep python
# Windows: tasklist | findstr python
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

- **Issues**: Create an issue on GitHub
- **Questions**: Check existing issues first
- **Documentation**: Read this README carefully

---

**Happy Coding! 🚀**

*Made with ❤️ for students and developers*