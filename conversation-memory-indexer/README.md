# conversation-memory-indexer

对话记忆索引系统 - 将每日对话转化为可检索的结构化索引

## 功能

自动从对话中提取话题、决策、关键词，生成结构化索引文件，实现：
- 93-96% 的 Token 节省
- 跨日话题关联检索
- 决策历史追踪

## 使用

在 daily-summary 任务中自动调用，或手动执行：

```bash
# 生成今日索引
node skills/conversation-memory-indexer/index.js --date $(date +%Y-%m-%d)

# 检索历史话题
node skills/conversation-memory-indexer/index.js --search "定时任务" --days 7
```

## 输出

- `memory/index/YYYY-MM-DD.json` - 结构化索引
- 支持按关键词、情感标记、决策类型检索

## 作者

Cypher - 学者型能力萃取
