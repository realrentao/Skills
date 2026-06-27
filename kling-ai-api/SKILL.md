---
name: kling-ai-api
description: >
  Kling AI (可灵) API 集成 — 文生视频、图生视频。国内站用户必须使用
  api-beijing.klingai.com 端点，JWT HMAC-SHA256 鉴权。
agent_created: true
---

# Kling AI (可灵) API 集成技能

## 用途

调用快手可灵 Kling AI 的 v3 文生视频 / 图生视频 API，生成高质量真实场景视频。
适用于制作 AI 视频内容，特别是替代 Ken Burns 缩放效果的真实视频生成场景。

## 触发条件

用户提到「可灵」「Kling」「文生视频」「可灵API」「国内站」等关键词时加载此技能。

## 核心信息

### 1. API 端点

| 用户类型 | 端点 | 说明 |
|---------|------|------|
| **国内用户** | `https://api-beijing.klingai.com` | 默认正确端点 |
| 国际用户 | `https://api.klingai.com` | 海外用户使用 |

**⚠️ 国内站用户不能用 `api.klingai.com` — 会返回 401 Auth failed。**

### 2. 鉴权方式

使用 **JWT HMAC-SHA256**，payload 结构如下：

```python
import jwt, time
payload = {
    "iss": ACCESS_KEY,      # Access Key ID
    "exp": int(time.time()) + 1800,   # 30分钟有效期
    "nbf": int(time.time()) - 5,      # 5秒前生效
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256",
                   headers={"alg": "HS256", "typ": "JWT"})
```

认证头：`Authorization: Bearer {token}`

### 3. 文生视频 API

**提交任务**: `POST /v1/videos/text2video`

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_name` | string | 是 | `kling-v1-6` (推荐) |
| `prompt` | string | 是 | 视频描述，最多2500字符 |
| `negative_prompt` | string | 否 | 排除内容 |
| `cfg_scale` | float | 否 | 0.0~1.0，默认0.5 |
| `duration` | string | 否 | `"5"` 或 `"10"` 秒 |
| `aspect_ratio` | string | 否 | `"16:9"`, `"9:16"`, `"1:1"` |
| `mode` | string | 否 | `"std"`(标准) / `"pro"`(专业) |

**轮询结果**: `GET /v1/videos/text2video/{task_id}`

返回 task_status: `submitted` → `processing` → `succeed` / `failed`

### 4. 常见错误

| HTTP状态码 | code | message | 原因 |
|-----------|------|---------|------|
| 200 | 0 | success | 正常 |
| 401 | 1002 | Auth failed | 鉴权失败，检查密钥或端点 |
| 429 | 1102 | Account balance not enough | 账户余额不足，需购买资源包 |
| 200 | 1001 | quota exceeded | 配额不足，需充值 |

### 5. 余额不足解决方案

返回 429 "Account balance not enough" 时：
1. 访问 https://klingai.kuaishou.com/ 登录
2. 进入 API 管理 → 资源包管理
3. 购买所需资源包（5秒 std 模式每次约 ¥0.14）

## 参考实现

完整工作脚本见 `kling_client.py`（项目目录下），包含：
- JWT Token 生成
- 任务提交与轮询
- 视频下载
- 错误处理

## 注意

- 视频生成是异步的，轮询间隔建议 5 秒以上
- std 模式 5 秒视频费用约为 pro 模式的一半
- 国内站 API Key 在 https://klingai.kuaishou.com/ 开发者平台创建
