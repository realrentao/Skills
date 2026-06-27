---
title: "手动保存 Cloud Profile"
description: "在会话结束前手动保存当前 profile 到本地，防止数据丢失"
agent_created: true
trigger:
  - "保存 profile"
  - "保存记忆"
  - "备份 memory"
  - "保存 cloud profile"
---

# 手动保存 Cloud Profile

当 WorkBuddy 每次重启后数据丢失或左侧项目回到几天前时，在关闭前手动执行以下操作：

## 步骤

1. **查找最新的 cloud profile**
   ```
   ls -lt "C:/Users/迪丽希斯/.workbuddy/memory/" | head -5
   ```

2. **复制备份到以今天日期命名的文件**
   ```
   cp 278b7de7-ce3a-46f9-9639-8036b3ec31b7_memory.md 278b7de7-ce3a-46f9-9639-8036b3ec31b7_memory_2026-06-27.md
   ```

3. **确认备份成功**
   ```
   ls -la "C:/Users/迪丽希斯/.workbuddy/memory/" | grep "2026-06-27"
   ```

## 注意

- 最新的 cloud profile UUID: `278b7de7-ce3a-46f9-9639-8036b3ec31b7`
- 如果 UUID 变化，使用最新的那个
- 每次会话结束前都执行一次，防止重启后数据丢失