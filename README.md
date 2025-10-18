# 🤖 hermes-2api: 你的私人赫尔墨斯信使

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)](https://github.com/lzA6/hermes-2api)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg?logo=docker)](https://hub.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg?logo=python)](https://www.python.org/)

**将 [Hermes](https://hermes.nousresearch.com) 的强大能力，转化为开发者友好的、兼容 OpenAI 格式的 API。**

[English](./README.en.md) | **中文**

---

> **💖 项目的核心理念与价值观**
>
> 在这个代码与数据交织的时代，我们每个人都是潜在的创造者。`hermes-2api` 的诞生，源于一个简单的信念：**技术不应被束之高阁，而应成为赋能每个人的工具。**
>
> 我们相信，通过分享、开源和协作，我们可以打破信息壁垒，让前沿的 AI 技术变得触手可及。这个项目不仅仅是一堆代码，它是一种姿态，一种邀请。它在说："嘿，朋友，你看，这东西很酷，但它并不神秘。你也可以驾驭它，创造出属于你自己的奇迹。"
>
> 我们希望每一位接触到 `hermes-2api` 的朋友，不仅能收获一个实用的工具，更能感受到开源精神的温度，点燃自己动手实践的热情。**你来，你也行！** 这不是一句口号，而是我们对每一位探索者的真诚鼓励。让我们一起，用代码为这个世界增添一抹亮色，用创造力书写属于我们的诗篇。✨

---

## ✨ 主要特性

*   **🚀 OpenAI 兼容**：无缝对接任何支持 OpenAI API 格式的客户端、库或应用
*   **📦 Docker 一键部署**：使用 Docker 和 Docker Compose，告别繁琐的环境配置，实现"开箱即用"
*   **💨 流式响应**：支持打字机效果的流式输出，提供与原生体验一致的实时交互感
*   **🛡️ 安全可控**：通过 `API_MASTER_KEY` 保护你的 API 端点，防止未经授权的访问
*   **☁️ 智能伪装**：内置 `cloudscraper`，能有效绕过 Cloudflare 等网站防护，像真人一样与 Hermes 服务"交谈"
*   **🛠️ 高度可扩展**：清晰的项目结构和代码，为你未来的二次开发和功能扩展铺平道路

## 🎯 核心架构

```mermaid
graph TB
    subgraph "客户端应用"
        A[OpenAI 兼容客户端] --> B[发送 OpenAI 格式请求]
    end

    subgraph "hermes-2api 服务"
        B --> C{Nginx 反向代理}
        C --> D[FastAPI 应用]
        D --> E{身份验证}
        E --> F[Hermes Provider]
        F --> G[格式转换]
        G --> H[Cloudscraper]
    end

    subgraph "上游服务"
        H --> I[hermes.nousresearch.com]
        I --> J[返回流式响应]
    end

    subgraph "响应流程"
        J --> K[SSE 格式转换]
        K --> L[返回 OpenAI 格式流]
        L --> M[客户端实时显示]
    end

    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style F fill:#e8f5e8
    style I fill:#fff3e0
```

## 🤔 它是如何工作的？(核心原理大白话)

想象一下，你想和一个只会说"赫尔墨斯语"（Hermes 网站的内部通信方式）的智慧老人（`hermes.nousresearch.com`）聊天。但你所有的聊天工具（比如各种 AI 应用）都只会说"世界通用语"（OpenAI API 格式）。

这时，`hermes-2api` 就扮演了一个**超级翻译官**兼**私人信使**的角色！

### 工作流程详解

1.  **接收你的信件** 📬：你的应用（客户端）用"世界通用语"向 `hermes-2api` 发送一个请求
2.  **翻译并递送** 🏃‍♂️：`hermes-2api` 收到后，立刻将你的请求翻译成"赫尔墨斯语"，并模仿成一个真实的用户，带着你的"小饼干"（`HERMES_COOKIE`）去拜访那位智慧老人
3.  **实时传话** 🗣️：智慧老人开始一句一句地回答，`hermes-2api` 则在旁边实时地将每一句话从"赫尔墨斯语"翻译回"世界通用语"，并立刻传回给你的应用
4.  **完美体验** 😄：最终，你的应用收到了流畅、实时的回复，感觉就像在直接和智慧老人聊天一样，完全不知道中间还有这么一位辛勤的"翻译官"！

**便利性与便捷性**：你无需改造任何现有的、基于 OpenAI 标准开发的应用，只需将 API 的地址和密钥指向 `hermes-2api`，即可立即享用 Hermes-2 模型的强大功能。这就是它的魔力所在！

## 🚀 快速开始：懒人一键通

适合已经安装好 `Git` 和 `Docker` 的朋友。只需三步，即刻启动！

### 1. 克隆仓库并进入目录
```bash
git clone https://github.com/lzA6/hermes-2api.git
cd hermes-2api
```

### 2. 配置环境变量
```bash
# 复制配置文件模板
cp .env.example .env

# 编辑配置文件，设置你的 Cookie 和 API 密钥
# 请使用你喜欢的编辑器编辑 .env 文件
```

### 3. 启动服务
```bash
docker-compose up -d
```

服务现在应该已经在你指定的端口（默认为 `8088`）上运行了。恭喜你，可以开始使用了！🎉

## 👨‍🏫 超详细新手教程 (保姆级)

别担心，即使你是第一次接触这些，跟着下面的步骤，你也能轻松搞定！

### 第 0 步：准备工作 (安装必备软件)

你需要先在你的电脑上安装两个"神器"：

*   **Git**：一个版本控制工具，用来下载代码。从 [官网](https://git-scm.com/downloads) 下载并安装
*   **Docker**：一个容器化平台，可以理解为一个能运行各种软件的"魔法盒子"。从 [官网](https://www.docker.com/products/docker-desktop/) 下载并安装

### 第 1 步：获取 Cookie（关键步骤）

1. 在浏览器中打开 [Hermes](https://hermes.nousresearch.com) 并登录
2. 按 `F12` 打开开发者工具，切换到 **Network** 标签页
3. 在聊天框发送任意消息，找到名为 `chat` 的请求
4. 复制 **Headers** 中的 **Cookie** 完整值

### 第 2 步：配置环境

```bash
# 1. 克隆项目
git clone https://github.com/lzA6/hermes-2api.git
cd hermes-2api

# 2. 创建配置文件
cp .env.example .env

# 3. 编辑 .env 文件，填入你的 Cookie
```

`.env` 文件示例：
```env
# API 主密钥，建议修改为复杂字符串
API_MASTER_KEY=your-secret-key-here

# Nginx 服务端口
NGINX_PORT=8088

# Hermes Cookie（从浏览器获取）
HERMES_COOKIE="your-cookie-value-here"
```

### 第 3 步：启动服务

```bash
# 使用 Docker Compose 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 第 4 步：测试 API

```bash
curl -X POST http://localhost:8088/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-secret-key-here" \
  -d '{
    "model": "DeepHermes-3-Llama-3-8B-Preview",
    "messages": [
      {
        "role": "user",
        "content": "你好，请介绍一下你自己"
      }
    ],
    "stream": true
  }'
```

如果看到流式输出，说明配置成功！🥳

## 🔧 技术架构详解

### 📂 项目结构

```
hermes-2api/
├── 📄 .env                    # 环境配置文件（需手动创建）
├── 📄 .env.example            # 环境配置示例
├── 📄 docker-compose.yml      # Docker 服务编排
├── 📄 Dockerfile              # 应用容器配置
├── 📄 main.py                 # FastAPI 主应用
├── 📄 nginx.conf              # Nginx 配置
├── 📄 requirements.txt        # Python 依赖
└── 📂 app/
    ├── 📂 core/
    │   └── 📄 config.py       # 配置管理
    ├── 📂 providers/
    │   ├── 📄 base_provider.py    # 提供商基类
    │   └── 📄 hermes_provider.py  # Hermes 提供商实现
    └── 📂 utils/
        └── 📄 sse_utils.py    # SSE 工具函数
```

### 🛠️ 技术栈

| 组件 | 用途 | 优势 |
|------|------|------|
| **FastAPI** | Web API 框架 | 高性能、自动文档、类型提示 |
| **Docker** | 容器化部署 | 环境隔离、一键部署 |
| **Nginx** | 反向代理 | 高性能、流式传输优化 |
| **Cloudscraper** | 反爬虫绕过 | 自动处理 Cloudflare 防护 |
| **Pydantic** | 数据验证 | 类型安全、配置管理 |

### 📜 核心代码解析

#### `main.py` - API 入口
```python
@app.post("/v1/chat/completions")
async def chat_completion(
    request: ChatCompletionRequest,
    api_key: str = Depends(verify_api_key)
):
    """处理聊天补全请求，支持流式响应"""
    provider = get_provider()
    if request.stream:
        return StreamingResponse(
            provider.chat_completion(request),
            media_type="text/event-stream"
        )
```

#### `hermes_provider.py` - 核心逻辑
```python
async def chat_completion(self, request: ChatCompletionRequest):
    """处理与 Hermes 服务的通信和格式转换"""
    async for chunk in self._stream_chat_completion(request):
        yield self._format_sse_chunk(chunk)
```

#### `nginx.conf` - 流式传输优化
```nginx
location / {
    proxy_pass http://hermes_backend;
    proxy_buffering off;  # 关键：禁用缓冲以实现实时流式传输
    proxy_set_header Host $host;
}
```

## 🎯 API 使用示例

### 基本聊天
```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8088/v1",
    api_key="your-secret-key-here"
)

response = client.chat.completions.create(
    model="DeepHermes-3-Llama-3-8B-Preview",
    messages=[
        {"role": "user", "content": "请用 Python 写一个快速排序算法"}
    ],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 系统提示词
```python
messages = [
    {
        "role": "system", 
        "content": "你是一个专业的 Python 开发助手，回答要简洁专业"
    },
    {
        "role": "user",
        "content": "如何优化 Python 代码的性能？"
    }
]
```

## 🔧 故障排除

### 常见问题

**1. Cookie 失效**
```
Error: 401 Unauthorized
```
解决方案：重新获取 HERMES_COOKIE 并更新 .env 文件

**2. 端口被占用**
```
Error: Port 8088 is already in use
```
解决方案：修改 .env 中的 NGINX_PORT 为其他端口

**3. 流式响应中断**
```
Error: Connection closed unexpectedly
```
解决方案：检查网络连接，确认 HERMES_COOKIE 有效

### 服务管理命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f app

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps
```

## 🌟 项目价值与局限

### 👍 核心价值

1. **生态兼容** - 无缝接入现有 OpenAI 生态
2. **部署简便** - Docker 一键部署，无需复杂环境配置
3. **实时体验** - 完整的流式传输支持
4. **学习参考** - 优秀的 API 网关和协议转换案例

### ⚠️ 当前局限

1. **Cookie 依赖** - 需要手动获取和更新 Cookie
2. **单点服务** - 依赖上游服务可用性
3. **功能基础** - 目前仅实现核心聊天功能

## 🔮 未来发展

### 🚀 规划中的特性

- [ ] **自动 Cookie 刷新** - 集成无头浏览器自动登录
- [ ] **多账号支持** - Cookie 池和负载均衡
- [ ] **使用量统计** - Token 计数和配额管理
- [ ] **Web 管理界面** - 可视化配置和监控
- [ ] **更多模型支持** - 扩展支持的模型列表

### 💡 贡献指南

我们欢迎所有形式的贡献！包括但不限于：

- 🐛 报告 Bug
- 📖 改进文档
- 🔧 提交代码修复
- 🎨 新增功能特性
- 💡 提出建议和想法

请参考 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细的贡献指南。

## 📜 开源协议

本项目采用 **Apache 2.0** 开源协议。

## 🤝 致谢

- 感谢 **Nous Research** 团队提供优秀的 Hermes 模型
- 感谢所有开源项目的贡献者
- 感谢每一位使用和支持本项目的用户

---

**用代码构建桥梁，让思想自由流淌。**

---

*如有问题或建议，请通过 [GitHub Issues](https://github.com/lzA6/hermes-2api/issues) 联系我们。*
