# Skill: Conversation Memory Indexer

## 触发条件

- 每日 22:00 定时任务自动生成
- 手动调用：需要回顾历史对话时

## 核心逻辑

### 1. 话题提取 (Topic Extraction)

从对话中识别独立话题单元：
- 话题边界：时间间隔 >30min 或主题切换
- 话题属性：标题、关键词、情感标记、参与者

### 2. 决策捕获 (Decision Capture)

识别并记录关键决策：
- 显式决策："决定...", "采用...", "暂停..."
- 隐式决策：任务触发、文件修改、状态变更

### 3. 索引生成 (Index Generation)

输出结构化 JSON：
```json
{
  "date": "YYYY-MM-DD",
  "topics": [...],
  "actions": {
    "tasksTriggered": [],
    "tasksPaused": [],
    "skillsCreated": [],
    "filesModified": []
  },
  "contextSnapshot": "一句话总结",
  "stats": { "totalTopics": 0 }
}
```

### 4. 检索接口 (Retrieval API)

```javascript
// 按关键词检索
recall.conversation({
  query: "定时任务",
  dateRange: ["2026-02-01", "2026-02-07"],
  includeDecisions: true
});

// 按情感标记检索
recall.bySentiment("problem-solving", 7);

// 跨日话题追踪
recall.topicChain("对话记忆索引");
```

## 依赖

- Node.js >= 18
- 目录权限：memory/index/

## 性能

- 生成时间：~500ms/日对话
- 检索延迟：<100ms
- Token 节省：93-96%

## Changelog

- v1.0.0 (2026-02-07): 初始版本，三层记忆架构
