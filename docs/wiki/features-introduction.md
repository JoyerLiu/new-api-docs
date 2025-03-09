# ✨ 特性说明

1. 🎨 全新的UI界面（部分界面还待更新）
2. 🌍 多语言支持（待完善）
3. 🎨 添加[Midjourney-Proxy(Plus)](https://github.com/novicezk/midjourney-proxy)接口支持
4. 💰 支持在线充值功能，可在系统设置中设置：
    - [x] 易支付
5. 🔍 支持用key查询使用额度：
    - 配合项目[neko-api-key-tool](https://github.com/Calcium-Ion/neko-api-key-tool)可实现用key查询使用
6. 📑 分页支持选择每页显示数量
7. 🔄 兼容原版One API的数据库，可直接使用原版数据库（one-api.db）
8. 💵 支持模型按次数收费，可在 系统设置-运营设置 中设置
9. ⚖️ 支持渠道 **加权随机**
10. 📈 数据看板（控制台）
11. 🔒 可设置令牌能调用的模型
12. 🤖 支持Telegram授权登录：
    1. 系统设置-配置登录注册-允许通过Telegram登录
    2. 对[@Botfather](https://t.me/botfather)输入指令/setdomain
    3. 选择你的bot，然后输入http(s)://你的网站地址/login
    4. Telegram Bot 名称是bot username 去掉@后的字符串
13. 🎵 添加 [Suno API](https://github.com/Suno-API/Suno-API)接口支持
14. 🔄 支持Rerank模型，目前兼容Cohere和Jina，可接入Dify
15. ⚡ **[OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime/integration)** - 支持OpenAI的Realtime API，支持Azure渠道
16. 支持使用路由/chat2link 进入聊天界面
17. 🧠 支持通过模型名称后缀设置 reasoning effort：
    1. OpenAI o系列模型
        - 添加后缀 `-high` 设置为 high reasoning effort (例如: `o3-mini-high`)
        - 添加后缀 `-medium` 设置为 medium reasoning effort (例如: `o3-mini-medium`)
        - 添加后缀 `-low` 设置为 low reasoning effort (例如: `o3-mini-low`)
    2. Claude 思考模型
        - 添加后缀 `-thinking` 启用思考模式 (例如: `claude-3-7-sonnet-20250219-thinking`)
18. 🔄 思考转内容，支持在 `渠道-编辑-渠道额外设置` 中设置 `thinking_to_content` 选项，默认`false`，开启后会将思考内容 `reasoning_content` 转换为 `<think>` 标签拼接到内容中返回。
19. 🔄 模型限流，支持在 `系统设置-速率限制设置` 中设置模型限流，支持设置总请求数限制和成功请求数限制
20. 💰 缓存计费支持，开启后可以在缓存命中时按照设定的比例计费：
    1. 在 `系统设置-运营设置` 中设置 提示缓存倍率 选项
    2. 在渠道中设置 提示缓存倍率，范围 0-1，例如设置为 0.5 表示缓存命中时按照 50% 计费
    3. 支持的渠道：
      - [x] OpenAI
      - [x] Azure
      - [x] DeepSeek
      - [ ] Claude