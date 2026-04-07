---
name: cypher-writing-qa
description: "MUST use when: (1) finalizing blog articles before publishing, (2) checking for AI-flavor content, (3) enforcing writing style consistency, (4) running quality checks on generated content. Triggers on phrases like 'check article', 'quality check', 'remove AI flavor', 'polish article', '质检文章'."
metadata:
  author: Cypher Team
  version: "1.0.0"
  license: MIT
  requires:
    bins: ["python3"]
  tags: ["writing", "qa", "quality", "style-check"]
---

# Cypher 写作质检器

四层自检体系，去除 AI 味，提升文章质量。

## When to Use

**MUST use when:**
- Finalizing blog articles before publishing
- Checking for AI-flavor content
- Enforcing writing style consistency
- Running quality checks on generated content

**Trigger phrases:**
- "check article"
- "quality check"
- "remove AI flavor"
- "polish article"
- "质检文章"
- "检查文章质量"

## Four-Layer QA System

```
┌─────────────────────────────────────────┐
│  L1: 硬性规则检查 (Auto)                │
│  - 禁用词扫描                           │
│  - 禁用标点扫描                         │
│  - 套话检测                             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  L2: 风格一致性检查 (Pattern)           │
│  - 开头检查                             │
│  - 节奏与结构                           │
│  - 口语化程度                           │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  L3: 内容质量检查 (Deep)                │
│  - 观点支撑                             │
│  - 知识输出方式                         │
│  - 文化升维                             │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  L4: 活人感终审 (Human)                 │
│  - 温度感                               │
│  - 独特性                               │
│  - 姿态                                 │
└─────────────────────────────────────────┘
```

## L1: 硬性规则检查

### 禁用词清单

| 禁用词 | 替换建议 |
|--------|---------|
| "说白了" | 坦率的讲、其实就是 |
| "意味着什么" / "这意味着" | 那结果会怎样呢、所以呢 |
| "本质上" | 说到底、其实 |
| "换句话说" | 你想想看、也就是说 |
| "不可否认" | 直接删掉，换成正面陈述 |
| "综上所述" / "总的来说" | 具体的回扣句 |
| "首先...其次...最后" | 自然转场词 |
| "值得注意的是" / "不难发现" | 直接说 |
| "让我们来看看..." | 删掉 |
| "接下来让我们..." | 删掉 |
| "在当今...的时代" | 删掉 |
| "随着...的发展" | 删掉 |

### 禁用标点

| 禁用 | 替换 |
|------|------|
| 冒号 ":" | 逗号 |
| 破折号 "——" | 逗号或句号 |
| 双引号 "" / "" | 「」或直接不加 |

### 空泛工具名

❌ 禁止："AI工具"、"某个模型"、"相关技术"
✅ 正确："Claude Code"、"GPT-4"、"DeepSeek"

## L2: 风格一致性检查

### 开头检查
- [ ] 从具体事件/场景切入（非宏大叙事）
- [ ] 第一句话让人产生"然后呢？"的冲动
- [ ] 无教科书式开头

### 节奏检查
- [ ] 长短句交替
- [ ] 至少 3 处"一句一段"的断裂效果
- [ ] 偏离主线后有"扣主线句"拉回来
- [ ] 使用疑问句制造节奏刹车

### 口语化检查
- [ ] 全文至少 8-10 个不同口语化表达
- [ ] 有论述中的故意打破
- [ ] 至少一处自嘲或承认不足
- [ ] 标点表达情绪（。。。？？？= =）

## L3: 内容质量检查

### 观点支撑
- [ ] 每个核心观点有具体人/场景/细节支撑
- [ ] 无空泛观点只有论断

### 知识输出
- [ ] 知识"聊着聊着顺手掏出"，非"下面介绍"
- [ ] 引用自然融入

### 文化升维
- [ ] 至少一处连接到更大文化/哲学/历史参照
- [ ] 连接自然

### 对立面与同理心
- [ ] 讲观点时理解对方立场
- [ ] 先站读者处境再给视角

## L4: 活人感终审

### 核心问题
> "读完这篇文章，我感觉是一个有见识的普通人在认真跟我聊一件打动他的事，还是一个AI在给我输出信息？"

### 感知维度
- **温度感**：体感记忆（"我当时就愣住了"）而非知识描述（"我感到震撼"）
- **独特性**：有"只有作者才会写的角度"
- **姿态**："有见识的普通人聊打动他的事"而非"导师教学生"
- **心流**：从头读到尾注意力是否断掉

## Quick Start

```bash
# 质检文章
python3 {baseDir}/scripts/qa_check.py --file /path/to/article.md

# 输出质检报告
python3 {baseDir}/scripts/qa_check.py --file article.md --output report.md

# 自动修复 L1 问题
python3 {baseDir}/scripts/qa_check.py --file article.md --fix-l1
```

## Integration in Pipeline

```bash
# 在 content-pipeline 中调用
# Phase 2: Writing → Phase 2.5: QA → Phase 3: Image

# Example:
python3 ~/.openclaw/skills/cypher-writing-qa/scripts/qa_check.py \
  --file /tmp/article.md \
  --strict-mode \
  --fail-on-l1
```

## QA Report Format

```markdown
## 质检报告

### L1 硬性规则 [✅/❌]
- 禁用词：X处命中
- 禁用标点：X处命中
- 结构套话：X处命中
- 空泛工具名：X处

### L2 风格一致性 [✅/❌]
- 开头：✅/❌
- 节奏：✅/❌
- 口语化：X个口语词组
- 标点禁令：✅/❌

### L3 内容质量 [✅/❌]
- 观点支撑：✅/❌
- 知识输出：✅/❌
- 文化升维：✅/❌
- 同理心：✅/❌

### L4 活人感 [✅/❌]
- 温度感：✅/❌
- 独特性：✅/❌
- 姿态：✅/❌
- 心流：✅/❌

**总评**: 4层通过 / X层需返工
**修复优先级**: 1. ... 2. ... 3. ...
```

## 推荐口语化词组

### 转场过渡
- 坦率的讲、说真的、我是真的觉得
- 怎么说呢、其实吧、你想想看
- 我跟你说、回到xxx这块
- 顺着上面的再聊聊

### 表达判断
- 我有时候觉得、我一直觉得
- 这话听着有点刺耳但
- 我自己的感受是、我始终坚信

### 承认自嘲
- 说实话我也不确定
- 我自己也还在摸索
- 可能有些想法还不成熟
- 这个事儿我也踩过坑

### 情绪表达
- 这种感觉太爽了
- 我当时就愣住了
- 想想就觉得兴奋
- 太离谱了

## Configuration

### 严格模式
```bash
--strict-mode  # L1 必须 100% 通过
--fail-on-l1   # L1 不通过则返回错误码
```

### 自定义规则
```yaml
# ~/.openclaw/config/writing-qa.yaml
banned_words:
  - "说白了"
  - "本质上"
banned_punctuation:
  - ":"
  - "——"
min_casual_phrases: 8
```

## Error Handling

| 阶段 | 问题 | 处理 |
|------|------|------|
| L1 | 命中禁用词 | 标记位置，建议替换 |
| L1 | 命中禁用标点 | 标记位置，建议替换 |
| L2 | 口语化不足 | 提示增加口语词组 |
| L2 | 节奏呆板 | 建议长短句交替 |
| L3 | 观点无支撑 | 建议补充案例 |
| L4 | AI 味重 | 整体重写建议 |

## References

- Inspired by: 数字生命卡兹克 (khazix-writer)
- Four-layer QA system from: https://github.com/KKKKhazix/khazix-skills
