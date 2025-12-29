# 🕵️ The Bias Detective (Rashomon Edition)

> **An AI-Powered Interface for Epistemic Diversity**  
> **一个用于探索认知多样性的 AI 增强工具**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://the-bias-detective.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The Bias Detective** is a cognitive tool designed to break echo chambers. Instead of giving you "the answer," it analyzes any news event or historical moment through **three distinct analytical lenses** simultaneously. Inspired by the *Rashomon Effect*, it forces us to confront the reality that truth is often a matter of perspective.

**偏见侦探** 是一个旨在打破回声室效应的认知工具。它不会直接给你“标准答案”，而是通过 **三个截然不同的分析透镜** 同时解构任何新闻事件或历史时刻。受“罗生门效应”启发，它迫使我们直面一个事实：真相往往取决于观察的角度。

---

## ✨ Key Features / 核心功能

- **⚡ Parallel Intelligence (并行智能)**  
  Utilizes `concurrent.futures` to dispatch AI agents into parallel dimensions. Analyzes all three perspectives simultaneously, reducing wait time from ~10s to ~3s.  
  利用并发处理技术，同时并行生成三个视角的分析，将等待时间大幅缩短，提供流畅的交互体验。

- **🎭 The "Rashomon" Engine (罗生门引擎)**  
  Three strictly prompt-engineered personas that never break character:
  - **🏛️ The Establishment (建制派)**: Focuses on order, law, and institutional continuity.
  - **💰 Follow the Money (金钱流向)**: Traces incentives, capital flows, and economic determinism.
  - **🎭 The Subtext (潜台词)**: Uses critical theory to expose power dynamics and marginalized voices.

- **🛡️ Privacy & Flexibility (隐私与灵活)**  
  **BYOK (Bring Your Own Key)** architecture. Your API key is never stored on a server. If no key is provided, the system gracefully degrades to **Mock Mode**, using academic-grade pre-written datasets for demonstration.  
  支持“自带密钥”模式，保护您的隐私。如果未提供密钥，系统将自动切换到 **演示模式 (Mock Mode)**，展示预设的学术级分析案例。

---

## 🚀 Quick Start / 快速开始

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/the-bias-detective.git
cd the-bias-detective
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. (Optional) Configure Environment
You can create a `.env` file in the root directory to store your API key for local development:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

---

## 📸 Screenshots / 界面预览

| **Analysis View** | **Sensemaking** |
|:---:|:---:|
| *Real-time parallel analysis with color-coded perspectives* | *Interactive synthesis to bridge the cognitive gap* |
| *实时并行分析与颜色编码的视角展示* | *交互式综合环节，弥合认知鸿沟* |

---

## 🛠️ Tech Stack / 技术栈

- **Frontend**: [Streamlit](https://streamlit.io/) (Python)
- **AI Engine**: OpenAI API (GPT-3.5/4)
- **Concurrency**: Python `concurrent.futures`
- **Deployment**: Streamlit Community Cloud

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
