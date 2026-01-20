# Botivate v1.0 - Frontend

A modern chat interface for the DB Assistant backend.

## 📁 Structure

```
Frontend/
├── index.html    # Main HTML file
├── styles.css    # CSS styles
├── app.js        # JavaScript logic
└── README.md     # This file
```

## 🚀 Running the Frontend

### Option 1: Through Backend (Recommended)

The backend serves the frontend automatically:

```bash
cd Backend
uvicorn src.main:app --reload --port 8000
```

Then open: **http://localhost:8000/app**

### Option 2: Live Server (VS Code)

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Make sure backend is running on port 8000

### Option 3: Direct File

1. Open `index.html` directly in browser
2. Make sure backend is running on port 8000

## ⚙️ Configuration

Edit `app.js` to change the backend URL:

```javascript
const API_BASE_URL = 'http://localhost:8000';  // Change this if needed
```

## ✨ Features

- **Modern Dark UI** - Beautiful purple-themed interface
- **Connection Status** - Real-time backend health monitoring
- **Sample Queries** - Quick start buttons for common questions
- **Language Support** - English and Hinglish queries
- **Voice Input** - Microphone support (Chrome/Edge)
- **Security Indicators** - Shows when queries are blocked
- **SQL Display** - Shows generated SQL for successful queries

## 🎨 Customization

### Colors (in `styles.css`)

```css
:root {
  --bg-dark: #0a0a0c;
  --accent-purple: #8b5cf6;
  --text-main: #ffffff;
  --text-dim: #94a3b8;
}
```

### Sample Queries (in `index.html`)

```html
<button class="sample-query" onclick="useSampleQuery('Your query here')">
  <i class="fas fa-icon"></i> Button Text
</button>
```

## 🔗 API Endpoints Used

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check backend status |
| POST | `/chat` | Send chat message |
