<p align="center">
  <img src="https://img.shields.io/badge/ASKY-Task%20Manager%20Bot-blue?style=for-the-badge&logo=telegram&logoColor=white" alt="ASKY Badge"/>
  <br/>
  <img src="https://img.shields.io/badge/python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/AI-Llama%203.3%2070B-orange?style=flat-square&logo=meta&logoColor=white" alt="Llama 3.3"/>
  <img src="https://img.shields.io/badge/Storage-Google%20Sheets-34A853?style=flat-square&logo=google-sheets&logoColor=white" alt="Google Sheets"/>
  <img src="https://img.shields.io/badge/Hosting-Telegram%20Bot%20API-26A5E4?style=flat-square&logo=telegram&logoColor=white" alt="Telegram"/>
</p>

---

# 📘 ASKY — AI-Powered Task Manager Bot

> **ASKY** is an intelligent Telegram bot that leverages natural language processing to help users manage their daily tasks. Users simply describe their tasks in plain language, and the AI extracts, categorizes, and stores them automatically in Google Sheets — no forms, no clicks, just conversation.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
  - [System Diagram](#system-diagram)
  - [Component Breakdown](#component-breakdown)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Bot](#running-the-bot)
- [Module Reference](#module-reference)
  - [`main.py` — Application Entry Point](#mainpy--application-entry-point)
  - [`src/ai_agent.py` — AI Task Parser](#srcai_agentpy--ai-task-parser)
  - [`src/sheets_manager.py` — Google Sheets Data Layer](#srcsheets_managerpy--google-sheets-data-layer)
  - [`src/telegram.py` — Telegram Bot Interface](#srctelegrampy--telegram-bot-interface)
- [User Flow](#user-flow)
  - [Adding Tasks](#adding-tasks)
  - [Viewing Tasks](#viewing-tasks)
  - [Completing Tasks](#completing-tasks)
  - [Daily Reminder](#daily-reminder)
- [Data Schema](#data-schema)
- [Environment Variables](#environment-variables)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Future Roadmap](#future-roadmap)
- [License](#license)

---

## Overview

ASKY bridges the gap between **unstructured human language** and **structured task management**. Instead of manually filling in task fields, users type naturally (e.g., _"I need to submit the report by Friday and call the client tomorrow"_), and the AI engine automatically:

1. **Extracts** individual tasks from the message.
2. **Infers** due dates and categories.
3. **Stores** everything into a Google Sheets spreadsheet for persistent tracking.
4. **Reminds** users of pending tasks every evening.

---

## Key Features

| Feature | Description |
|---|---|
| 🧠 **AI-Powered Parsing** | Uses Groq's Llama 3.3 70B model to extract up to 10 tasks from a single natural language message. |
| 📊 **Google Sheets Backend** | All tasks are stored in a Google Sheets spreadsheet — easy to view, share, and collaborate on. |
| ✅ **Bulk Task Completion** | Select and mark multiple tasks as done simultaneously through an interactive inline keyboard. |
| 🔔 **Scheduled Reminders** | Automatic daily reminder at **17:45** with a summary of active tasks. |
| 🎯 **Category Detection** | AI automatically categorizes each task (e.g., Work, Personal, Study). |
| 💬 **Conversational UX** | Minimal UI — interact entirely through Telegram chat with intuitive reply keyboards. |

---

## Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          ASKY SYSTEM                                │
│                                                                     │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────────────┐ │
│  │ Telegram │◄──►│  ASKYBot     │◄──►│     SheetsManager          │ │
│  │   User   │    │ (telegram.py)│    │  (sheets_manager.py)       │ │
│  └──────────┘    └──────┬───────┘    └─────────────┬──────────────┘ │
│                         │                          │                │
│                         │                          │                │
│                         ▼                          ▼                │
│                  ┌──────────────┐         ┌────────────────┐        │
│                  │   AIAgent    │         │  Google Sheets  │        │
│                  │(ai_agent.py) │         │  (Cloud Store)  │        │
│                  └──────┬───────┘         └────────────────┘        │
│                         │                                           │
│                         ▼                                           │
│                  ┌──────────────┐                                    │
│                  │  Groq API    │                                    │
│                  │ (Llama 3.3)  │                                    │
│                  └──────────────┘                                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | File | Responsibility |
|---|---|---|
| **Entry Point** | `main.py` | Bootstraps all services and starts the bot. |
| **AI Engine** | `src/ai_agent.py` | Parses natural language into structured task JSON via Groq API. |
| **Data Layer** | `src/sheets_manager.py` | CRUD operations on Google Sheets (save, read, update tasks). |
| **Bot Interface** | `src/telegram.py` | Telegram command handlers, inline keyboards, and scheduled reminders. |
| **Configuration** | `configs/.env` | Stores API keys and secrets. |
| **Credentials** | `configs/creds.json` | Google Cloud service account credentials for Sheets API access. |

---

## Tech Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Runtime** | Python | 3.10+ | Core language |
| **Bot Framework** | pyTelegramBotAPI | 4.26.0 | Telegram Bot API wrapper |
| **AI / LLM** | Groq SDK | 0.15.0 | Interface to Llama 3.3 70B Versatile |
| **Database** | gspread | 6.1.4 | Google Sheets API client |
| **Auth** | google-auth | 2.37.0 | Google Cloud service account authentication |
| **Config** | python-dotenv | 1.0.1 | Environment variable management |

---

## Project Structure

```
ASKY/
├── main.py                  # 🚀 Application entry point
├── requirements.txt         # 📦 Python dependencies
├── .gitignore               # 🔒 Git exclusion rules
├── ASKY.code-workspace      # 🛠️ VS Code workspace config
├── DOCUMENTATION.md         # 📘 This file
│
├── configs/                 # ⚙️ Configuration & secrets
│   ├── .env                 #    Environment variables (API keys, IDs)
│   └── creds.json           #    Google Cloud service account credentials
│
└── src/                     # 📂 Source code package
    ├── __init__.py           #    Package initializer
    ├── ai_agent.py           #    🧠 AI task parsing engine
    ├── sheets_manager.py     #    📊 Google Sheets data operations
    └── telegram.py           #    💬 Telegram bot UI & logic
```

---

## Getting Started

### Prerequisites

Before setting up ASKY, ensure you have:

- [x] **Python 3.10+** installed ([download](https://www.python.org/downloads/))
- [x] **A Telegram Bot Token** — obtained from [@BotFather](https://t.me/BotFather) on Telegram
- [x] **A Google Cloud Project** with the **Google Sheets API** and **Google Drive API** enabled
- [x] **A Google Cloud Service Account** with a downloaded `creds.json` key file
- [x] **A Groq API Key** — obtained from [Groq Console](https://console.groq.com/)
- [x] **A Google Spreadsheet** shared with the service account email address

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd ASKY

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

#### Step 1 — Create the Environment File

Create a file at `configs/.env` with the following variables:

> [!WARNING]
> **Do NOT commit this file to Git.** It is already listed in `.gitignore`. Always double-check before pushing.

```ini
TELEGRAM_TOKEN=<your_telegram_bot_token>
SPREADSHEET_ID=<your_google_spreadsheet_id>
MY_CHAT_ID=<your_telegram_chat_id>
GROQ_API_KEY=<your_groq_api_key>
```

> [!IMPORTANT]
> The `SPREADSHEET_ID` is the long alphanumeric string in your Google Sheets URL:
> `https://docs.google.com/spreadsheets/d/`**`THIS_PART`**`/edit`

> [!TIP]
> To find your `MY_CHAT_ID`, send a message to [@userinfobot](https://t.me/userinfobot) on Telegram.

#### Step 2 — Add Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → **IAM & Admin** → **Service Accounts**.
2. Create a service account (or use an existing one).
3. Generate a JSON key and save it as `configs/creds.json`.
4. **Share your Google Spreadsheet** with the service account email (found in `creds.json` under `client_email`).

### Running the Bot

```bash
python main.py
```

If configured correctly, you should see:

```
[LOG] Notification scheduler active for ***...
[LOG] Bot ASKY active ...
```

---

## Module Reference

### `main.py` — Application Entry Point

The orchestrator that initializes all components and starts the bot.

```python
# Simplified flow
SheetsManager()  →  AIAgent()  →  ASKYBot(ai, sm)  →  app.run()
```

| Step | Action |
|---|---|
| 1 | Loads environment variables from `configs/.env` |
| 2 | Initializes `SheetsManager` (connects to Google Sheets) |
| 3 | Initializes `AIAgent` (configures Groq LLM client) |
| 4 | Initializes `ASKYBot` with both dependencies injected |
| 5 | Calls `app.run()` to start Telegram polling |

---

### `src/ai_agent.py` — AI Task Parser

The intelligence layer that transforms free-form text into structured task objects.

#### Class: `AIAgent`

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `__init__()` | — | — | Initializes Groq client with `llama-3.3-70b-versatile` model and system prompt. |
| `parse(text)` | `text: str` | `list[dict]` | Sends user text to the LLM, returns up to 10 parsed task objects. |

#### AI System Prompt (Context)

The AI is instructed to:
- Extract up to **10 task items** from the user's input.
- Return a **JSON object** with a `tasks` key containing an array.
- Each task has: `task` (name), `date` (YYYY-MM-DD), `category` (auto-detected).
- Default to **today's date** if no date is mentioned.
- Return **pure JSON only** — no additional text.

#### Example Input / Output

```
Input:  "Submit the quarterly report by next Monday and schedule a team meeting"

Output: {
  "tasks": [
    {"task": "Submit the quarterly report", "date": "2026-02-23", "category": "Work"},
    {"task": "Schedule a team meeting",     "date": "2026-02-17", "category": "Work"}
  ]
}
```

---

### `src/sheets_manager.py` — Google Sheets Data Layer

Handles all persistent storage operations through the Google Sheets API.

#### Class: `SheetsManager`

| Method | Parameters | Returns | Description |
|---|---|---|---|
| `__init__()` | — | — | Authenticates with Google, opens the spreadsheet, and auto-creates headers if the sheet is empty. |
| `save_tasks(tasks)` | `tasks: list[dict]` | `dict \| False` | Batch-appends multiple task rows to the spreadsheet. |
| `get_tasks(days)` | `days: int = 30` | `list[dict]` | Retrieves all active (non-"Done") tasks within the specified day range. |
| `mark_done_bulk(task_names)` | `task_names: list[str]` | `bool` | Marks multiple tasks as "Done" by updating their Status column. |

#### Auto-Initialization

On first run, `SheetsManager` checks if the spreadsheet is empty. If so, it automatically inserts the header row:

| Column A | Column B | Column C | Column D | Column E |
|---|---|---|---|---|
| Timestamp | Tanggal Tugas | Nama Tugas | Status | Category |

---

### `src/telegram.py` — Telegram Bot Interface

The presentation layer that manages all user interactions through the Telegram Bot API.

#### Class: `ASKYBot`

| Method | Parameters | Description |
|---|---|---|
| `__init__(ai, sm)` | `ai: AIAgent`, `sm: SheetsManager` | Initializes bot, dependencies, user state stores, and starts the reminder scheduler. |
| `reminder_loop()` | — | Background thread that sends a daily task summary at **17:45**. |
| `show_selection_menu(chat_id, tasks, message_id)` | `chat_id: int`, `tasks: list`, `message_id: int \| None` | Renders an interactive checklist of tasks with toggle buttons. |
| `run()` | — | Registers all command/message handlers and starts infinite polling. |

#### Registered Handlers

| Trigger | Type | Action |
|---|---|---|
| `/start` | Command | Displays the main reply keyboard with three options. |
| `/stop` | Command | Removes the keyboard and stops the bot for the user. |
| `➕ Tambah Tugas` | Button | Enters task-input mode; awaits free-form text. |
| `📋 Cek Tugas` | Button | Retrieves and displays the 10 nearest active tasks. |
| `✅ Selesaikan Tugas` | Button | Displays an interactive multi-select checklist. |
| Free-form text | Message | Parsed by AI when in task-input mode. |
| `save_task` | Callback | Saves AI-parsed tasks to Google Sheets. |
| `confirm_bulk` | Callback | Marks selected tasks as "Done" in Google Sheets. |
| `cancel_done` / `cancel_task` | Callback | Cancels the current operation. |
| `select_<name>` | Callback | Toggles task selection in the completion menu. |

#### State Management

The bot uses three in-memory dictionaries to track user state per session:

```python
self.user_modes = {}   # Tracks if user is in 'waiting_task' mode
self.temp_add   = {}   # Holds AI-parsed tasks pending confirmation
self.temp_done  = {}   # Holds selected tasks pending bulk completion
```

> [!NOTE]
> State is stored in-memory and will reset if the bot restarts. This is acceptable for a single-user or small-group bot.

---

## User Flow

### Adding Tasks

```
User                              Bot                               AI                  Sheets
 │                                 │                                 │                    │
 │  ➕ Tambah Tugas                │                                 │                    │
 │ ──────────────────────────────► │                                 │                    │
 │                                 │  "Tugas apa yang ingin Anda     │                    │
 │  ◄─────────────────────────────  │   tambahkan hari ini?"         │                    │
 │                                 │                                 │                    │
 │  "Submit report by Friday       │                                 │                    │
 │   and call client tomorrow"     │                                 │                    │
 │ ──────────────────────────────► │  ──── parse(text) ────────────► │                    │
 │                                 │  ◄── [{task, date, category}] ─ │                    │
 │                                 │                                 │                    │
 │  ◄── "Konfirmasi 2 Tugas Baru"  │                                │                    │
 │      [✅ Simpan] [❌ Batal]      │                                │                    │
 │                                 │                                 │                    │
 │  ✅ Simpan                      │                                 │                    │
 │ ──────────────────────────────► │  ─────── save_tasks() ─────────────────────────────► │
 │                                 │  ◄──────────── OK ──────────────────────────────────  │
 │  ◄── "Berhasil disimpan!"       │                                │                    │
```

### Viewing Tasks

```
User                              Bot                                Sheets
 │                                 │                                   │
 │  📋 Cek Tugas                   │                                   │
 │ ──────────────────────────────► │  ──── get_tasks(30) ────────────► │
 │                                 │  ◄── [task1, task2, ...] ──────── │
 │  ◄── "📋 Daftar 10 Tugas        │                                  │
 │       Terdekat: ..."            │                                   │
```

### Completing Tasks

```
User                              Bot                                Sheets
 │                                 │                                   │
 │  ✅ Selesaikan Tugas            │                                   │
 │ ──────────────────────────────► │  ──── get_tasks(30) ────────────► │
 │                                 │  ◄── [task1, task2, ...] ──────── │
 │  ◄── Interactive checklist      │                                   │
 │      [  ] Task A                │                                   │
 │      [  ] Task B                │                                   │
 │      [🚀 Konfirmasi] [❌ Batal] │                                   │
 │                                 │                                   │
 │  Tap Task A  (toggle ✅)        │                                   │
 │ ──────────────────────────────► │  (menu refreshes with ✅ Task A)  │
 │                                 │                                   │
 │  🚀 Konfirmasi Selesai         │                                   │
 │ ──────────────────────────────► │  ── mark_done_bulk(["A"]) ──────►│
 │                                 │  ◄──────── OK ──────────────────  │
 │  ◄── "1 Tugas berhasil          │                                  │
 │       diselesaikan!"            │                                   │
```

### Daily Reminder

```
Background Thread                 Bot                             User
 │                                 │                                │
 │  (Clock hits 17:45)             │                                │
 │ ──────────────────────────────► │                                │
 │                                 │  ── get_tasks(30)[:5] ──►     │
 │                                 │  ◄── [active tasks] ────      │
 │                                 │                                │
 │                                 │  "🔔 Pengingat Sore (17:45):  │
 │                                 │   • Task A (2026-02-18)       │
 │                                 │   • Task B (2026-02-20)"      │
 │                                 │ ─────────────────────────────►│
```

---

## Data Schema

### Google Sheets — Primary Sheet (`sheet1`)

| Column | Header | Type | Description | Example |
|---|---|---|---|---|
| A | `Timestamp` | `datetime` | When the task was added | `2026-02-17 20:30:00` |
| B | `Tanggal Tugas` | `date` | Task due date (YYYY-MM-DD) | `2026-02-20` |
| C | `Nama Tugas` | `string` | Task name/description | `Submit quarterly report` |
| D | `Status` | `enum` | Task status: `Pending` or `Done` | `Pending` |
| E | `Category` | `string` | Auto-detected task category | `Work` |

---

## Environment Variables

| Variable | Required | Description | Example |
|---|---|---|---|
| `TELEGRAM_TOKEN` | ✅ | Telegram Bot API token from @BotFather | *(obtain from @BotFather)* |
| `SPREADSHEET_ID` | ✅ | Google Sheets document ID | *(from your Sheets URL)* |
| `MY_CHAT_ID` | ✅ | Telegram chat ID for the daily reminder recipient | *(from @userinfobot)* |
| `GROQ_API_KEY` | ✅ | Groq API key for accessing Llama 3.3 70B | *(from console.groq.com)* |

---

## Security Considerations

> [!CAUTION]
> **This project is designed for public GitHub hosting.** Never commit sensitive files to version control. The `.gitignore` is pre-configured to exclude them. Always verify with `git status` before pushing.

> [!IMPORTANT]
> Before publishing to GitHub, ensure the following files are **NOT** tracked:
> - `configs/.env` — contains all API keys and tokens
> - `configs/creds.json` — contains Google Cloud private key

| File | Status | Reason |
|---|---|---|
| `configs/.env` | 🔒 Git-ignored | Contains API keys and tokens |
| `configs/creds.json` | 🔒 Git-ignored | Google Cloud service account private key |
| `.venv/` | 🔒 Git-ignored | Virtual environment (large, not portable) |
| `__pycache__/` | 🔒 Git-ignored | Python bytecode cache |

### Best Practices

- **Rotate API keys** periodically, especially if they are accidentally exposed.
- **Restrict service account permissions** to only the necessary Google Sheets and Drive scopes.
- **Use `MY_CHAT_ID`** to limit reminder notifications to authorized users only.
- **Never hardcode secrets** in source files — always use environment variables.

---

## Troubleshooting

| Symptom | Probable Cause | Solution |
|---|---|---|
| `ModuleNotFoundError` | Virtual environment not activated or dependencies not installed | Run `.venv\Scripts\activate` then `pip install -r requirements.txt` |
| `CRITICAL_STOP: ...` on startup | Missing or invalid environment variables | Verify all values in `configs/.env` are correct |
| Bot doesn't respond to messages | Invalid `TELEGRAM_TOKEN` | Regenerate the token via @BotFather and update `.env` |
| `Error in AIAgent: ...` | Groq API key invalid or rate limit exceeded | Verify `GROQ_API_KEY` in `.env`; check [Groq status](https://status.groq.com/) |
| `Error Sheets: ...` | Google Sheets API auth failure | Ensure `creds.json` is valid and the spreadsheet is shared with the service account |
| `BadRequest: Message is not modified` | Editing a message with identical content | Already handled in code — safe to ignore |
| Reminder not sending at 17:45 | `MY_CHAT_ID` not set or incorrect | Update `MY_CHAT_ID` in `.env` with your Telegram chat ID |
| Tasks not appearing in Sheets | Spreadsheet not shared with service account | Share the spreadsheet with the `client_email` from `creds.json` |

---

## Future Roadmap

| Priority | Feature | Description |
|---|---|---|
| 🔴 High | **Multi-User Support** | Persistent user state (database-backed) to handle concurrent users. |
| 🔴 High | **Task Editing** | Allow users to modify task names, dates, and categories after creation. |
| 🟡 Medium | **Priority Levels** | Add High / Medium / Low priority to tasks with color-coded indicators. |
| 🟡 Medium | **Recurring Tasks** | Support for daily, weekly, or monthly recurring tasks. |
| 🟢 Low | **Timezone Support** | Per-user timezone configuration for accurate reminders. |
| 🟢 Low | **Analytics Dashboard** | Weekly/monthly task completion statistics and productivity insights. |
| 🟢 Low | **Multi-Language** | Support for English and other languages alongside Indonesian. |

---

## License

This project is private and intended for personal use. If you plan to open-source it, consider adding an [MIT](https://choosealicense.com/licenses/mit/) or [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) license.

---

<p align="center">
  <sub>📘 Documentation generated on <b>2026-02-17</b> · Built with ❤️ by the ASKY team</sub>
</p>
