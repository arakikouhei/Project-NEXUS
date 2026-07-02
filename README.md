# Project NEXUS

Project NEXUS is a personal AI assistant platform built from scratch in Python.

The goal of this project is to create a long-term AI system capable of memory, conversation, multiple AI engines, and eventually voice, vision, and robotics.

---

# Features

- ✅ Local AI powered by Ollama + Qwen
- ✅ Memory System
- ✅ Conversation Memory
- ✅ Prompt System
- ✅ AI Engine Switching
- ✅ JSON Persistent Memory
- ✅ Modular Architecture

---

# Architecture

```
User
 │
 ▼
Console
 │
 ▼
AIManager
 ├── MemoryManager
 ├── ConversationMemory
 └── QwenEngine
        │
        ▼
     Ollama
        │
        ▼
      Qwen3
```

---

# Project Structure

```
Project-NEXUS
├── config/
├── data/
├── docs/
├── logs/
├── nexus/
│   ├── ai/
│   ├── core/
│   └── memory/
├── prompts/
├── tests/
├── console.py
├── main.py
└── README.md
```

---

# Requirements

- Python 3.13+
- Ollama
- Qwen3
- requests

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run

```bash
python3 main.py
```

---

# Roadmap

## Version 1.x

- Prompt System
- Conversation Memory
- Better Error Handling
- Documentation

## Version 2.x

- Gemini Integration
- AI Router
- Web Search
- Tool System
- Voice Input / Output
- Camera Support
- Sphere AI Hardware

---

# License

MIT License (planned)