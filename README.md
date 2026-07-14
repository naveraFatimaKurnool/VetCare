# VetCare Chatbot

AI-powered chatbot for Meadow Vet Care clinic, built with Python, FastAPI, MCP (Model Context Protocol), and OpenAI GPT-4.

## Features

- **Service Information**: Search and filter veterinary services by category, species, and price
- **Appointment Booking**: Book appointments with real-time availability checks
- **Special Offers**: View current promotions and discounts
- **Natural Language Interface**: Chat with the bot using natural language

## Tech Stack

- **Backend**: Python + FastAPI
- **MCP Server**: FastMCP (Model Context Protocol)
- **Database**: Google Sheets (via gspread)
- **LLM**: OpenAI GPT-4
- **Frontend**: HTML/CSS/JavaScript

## Project Structure

```
VetCare/
├── mcp_server/
│   ├── __init__.py
│   ├── server.py          # MCP server with tools
│   ├── tools.py           # Tool definitions
│   └── sheets_client.py   # Google Sheets client
├── chatbot/
│   ├── __init__.py
│   ├── app.py             # FastAPI web app
│   ├── llm.py             # OpenAI integration
│   └── prompts.py         # System prompts
├── static/
│   ├── css/style.css
│   └── js/chat.js
├── templates/
│   └── index.html
├── credentials/           # Your Google Sheets credentials
├── main.py               # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/naveraFatimaKurnool/VetCare.git
cd VetCare
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_SHEETS_CREDENTIALS=credentials/service_account.json
SPREADSHEET_ID=1JhSODtviGHzXru6Eb5MhfXfVIF5vtJk3pclzzv7j2l4
```

### 4. Add Google Sheets Credentials

Place your Google Sheets service account JSON file in the `credentials/` folder:

```
credentials/service_account.json
```

### 5. Run the Application

```bash
python main.py
```

Open your browser and navigate to: http://localhost:8000

## MCP Tools Available

| Tool | Description |
|------|-------------|
| `search_services` | Search services by keyword |
| `filter_services` | Filter by category, species, price |
| `get_service_details` | Get details for a specific service |
| `check_availability` | Check available appointment slots |
| `get_categories` | List all service categories |
| `get_species_options` | List available animal species |
| `get_special_offers` | View current promotions |
| `get_available_services` | Services with open slots |
| `book_appointment` | Book an appointment |

## Google Sheets Format

The spreadsheet should have the following columns:

| Column | Description |
|--------|-------------|
| service_id | Unique identifier (e.g., MVC-001) |
| category | Service category |
| species | Target animal species |
| price_eur | Price in EUR |
| duration_min | Duration in minutes |
| requires_appointment | Yes/No |
| availability | Days/hours available |
| slots_this_week | Available slots |
| special_offer | Current promotion (optional) |
| service_name | Service name |
| description | Service description |

## API Endpoints

- `GET /` - Chat interface
- `POST /api/chat` - Send message to chatbot
- `POST /api/reset` - Reset conversation
- `GET /api/tools` - List available tools
- `GET /api/health` - Health check

## License

MIT
