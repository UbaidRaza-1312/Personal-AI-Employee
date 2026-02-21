# Bronze Tier AI Employee

An automated file processing system that leverages AI (Qwen) to handle incoming tasks, create action plans, and execute work autonomously.

## 🎯 Overview

This Bronze Tier system provides a simple yet powerful workflow for AI-assisted task processing:

1. **Drop files** into the `Inbox/` folder
2. **Automatic detection** moves files to `Needs_Action/` with metadata
3. **Orchestrator prompts** guide Qwen to process tasks
4. **Plans are created** and executed automatically
5. **Dashboard updates** track all activity
6. **Completed work** moves to `Done/`

## 📁 Project Structure

```
bronze/
├── Inbox/              # Drop zone for new files
├── Needs_Action/       # Files awaiting AI processing
├── Done/               # Completed work
├── Plans/              # Action plans created by Qwen
├── Skills/             # Skill definitions
├── Logs/               # System logs
├── orchestrator.py     # Main orchestration loop
├── filesystem_watcher.py # Inbox monitoring service
├── Dashboard.md        # Real-time status overview
└── Company_Handbook.md # Operating principles
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Qwen AI access (via VS Code or other interface)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bronze
```

2. Install dependencies:
```bash
pip install watchdog
```

### Running the System

**Terminal 1 - Start the Filesystem Watcher:**
```bash
python filesystem_watcher.py
```

**Terminal 2 - Start the Orchestrator:**
```bash
python orchestrator.py
```

## 📖 How It Works

### 1. File Drop
- Place any file in the `Inbox/` folder
- The filesystem watcher detects new files instantly

### 2. Automatic Processing
- File is copied to `Needs_Action/` with a unique name (`FILE_YYYYMMDD_HHMMSS_<original>`)
- A metadata file (`.md`) is created alongside it

### 3. Orchestrator Detection
- Every 30 seconds, the orchestrator checks `Needs_Action/`
- When files are found, it generates a Qwen prompt

### 4. AI Processing
- Copy the generated prompt into Qwen chat
- Qwen reads metadata, analyzes files, and creates plans
- Work is executed according to the plans

### 5. Completion
- Dashboard is updated with activity
- Files are moved to `Done/`
- System ready for next task

## 🔧 Configuration

### Orchestrator Settings

Edit `orchestrator.py` to customize:

```python
check_interval = 30  # Check interval in seconds
```

### Skill Definitions

Skills are defined in `Skills/` folder. Each skill describes:
- Purpose and trigger conditions
- Step-by-step workflow
- Output checklist
- Examples

## 📊 Dashboard

The `Dashboard.md` provides real-time visibility:

| Metric | Count |
|--------|-------|
| 📥 Inbox Items | Tracked |
| ⚠️ Needs Action | Tracked |
| ✅ Completed | Tracked |
| 📋 Active Plans | Tracked |

## 🏗️ Company Handbook

The `Company_Handbook.md` defines core operating principles:

1. **Always Read Metadata First** - Context is critical
2. **Think Before Acting** - Plan before execution
3. **One File, One Plan** - Clear traceability
4. **Update the Dashboard** - Maintain visibility
5. **Ask When Uncertain** - Flag for review when needed
6. **Preserve Original Files** - Maintain audit trails
7. **Work Sequentially** - First-in, first-out processing

## 🛠️ Development

### Adding New Skills

1. Create a new `.md` file in `Skills/`
2. Define purpose, triggers, and workflow
3. Reference the skill in orchestrator prompts

### Extending the Orchestrator

Modify `generate_qwen_prompt()` in `orchestrator.py` to:
- Add new processing steps
- Customize output formats
- Integrate additional tools

## 📝 Example Workflow

**Input:** User drops `meeting_notes.txt` in `Inbox/`

**System Creates:**
- `Needs_Action/FILE_20260219_174938_meeting_notes.txt`
- `Needs_Action/FILE_20260219_174938_meeting_notes.txt.md`

**Qwen Creates:**
- `Plans/PLAN_20260219_SummarizeMeeting.md`

**Output:**
- Summary document in `Done/`
- Dashboard updated
- Original files archived

## 🤝 Contributing

This is a Bronze Tier implementation. Future tiers may include:
- Silver: Direct API integration with Qwen
- Gold: Full autonomous execution without manual prompts
- Platinum: Multi-agent collaboration

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- Built for use with Qwen AI
- Inspired by autonomous agent architectures
- Designed for incremental automation

---

**Version:** 1.0 (Bronze Tier)  
**Status:** Active Development
