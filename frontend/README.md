# 🚀 AI 营销内容创作助手 (AI Content Agent)

> 面向流媒体/自媒体营销的智能化内容生产工具，基于 RAG 思维与 Prompt Engineering 构建。  

## 📺 项目演示视频
<video controls src="QQ202634-234726.mp4" title="Title"></video>

---

## 👥 团队分工 (共8人)

本项目采用**全栈功能分组**开发模式，分为 4 个核心小组并行开发：

| 小组名称 | 成员名单 | 核心职责 |
| :--- | :--- | :--- |
| **基建与架构组** | **张梓昂**、**李芷涵** | 后端基础架构搭建、数据库设计 (Models)、统一响应规范、Git 协作流管理 |
| **素材管理组** | **王皓群**、**李京赢** | 营销素材库的前后端开发、模板 CRUD 逻辑、Prompt 结构设计 |
| **AI 核心业务组** | **代睿涵**、**石昊宇** | 大模型接口对接、Prompt 动态拼接算法、流式生成逻辑、Loading 交互 |
| **记录与统计组** | **杨舒雅**、**彭乔茜** | 创作历史的全流程记录、数据持久化存储、可视化图表展示、首页看板 |

---

## ✨ 核心功能亮点

1.  **结构化模板引擎**：支持 9 大维度（身份、风格、平台、情绪等）的 Prompt 定义，而非简单的文本拼接。
2.  **智能内容生成**：深度对接 DeepSeek 大模型，自动根据模板和关键词生成抖音/小红书等平台的爆款文案。
3.  **零配置开箱即用**：内置环境配置与数据库初始化逻辑，启动即用。
4.  **全流程数据留痕**：自动保存每一次生成结果，支持按时间、关键词回溯历史创作。

---

## 🛠️ 技术栈

- **前端 (Frontend)**：Vue 3 + Vite + Element Plus + Axios
- **后端 (Backend)**：Python FastAPI + SQLAlchemy + Pydantic
- **数据库 (Database)**：SQLite (轻量级，无需安装数据库软件)
- **AI 模型**：DeepSeek V3 (兼容 OpenAI SDK)

---

## ⚡️ 快速启动指南 (Quick Start)

> **⚠️ 说明**：本项目已内置 `.env` 配置文件和预置数据库，老师/助教下载后可直接运行，无需申请 API Key。

### 第一步：启动后端 (Backend)

1.  进入后端目录：
    ```bash
    cd backend
    ```

2.  安装依赖库：
    ```bash
    pip install -r requirements.txt
    ```

3.  **启动服务**：
    *   推荐直接运行 `main.py` 文件来启动后端服务。
    *   (或者在 IDE 中右键 `main.py` -> Run)
    ```bash
    python main.py
    ```
    *   *看到 "Uvicorn running on http://127.0.0.1:8080" 即代表启动成功。*

### 第二步：启动前端 (Frontend)

1.  打开一个新的终端窗口，进入前端目录：
    ```bash
    cd frontend
    ```

2.  安装依赖：
    ```bash
    npm install
    ```

3.  启动页面：
    ```bash
    npm run dev
    ```

4.  **访问项目**：
    打开浏览器访问终端显示的地址（通常为 `http://localhost:5173`）。

---
