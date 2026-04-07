---
name: cypher-content-pipeline
description: "MUST use when: (1) creating complete blog articles from research to publishing, (2) generating daily AI reports or news briefings, (3) managing end-to-end content creation workflow, (4) coordinating research, writing, image generation, and publishing sub-tasks. Triggers on phrases like 'create article', 'generate daily report', 'run content pipeline', or scheduled content tasks."
metadata:
  author: Cypher Team
  version: "2.1.0"
  license: MIT
  requires:
    skills: ["cypher-research-assistant", "cypher-writing-qa", "cypher-image-pipeline", "cypher-publish-pipeline"]
    bins: ["git", "picgo"]
  tags: ["content", "pipeline", "workflow", "automation"]
---

# Cypher 内容创作流水线

End-to-end content creation pipeline with four-layer QA.

## What's New in v2.1

- ✅ **新增 Phase 2.5: 四层质检** - 基于卡兹克写作法的 L1-L4 质检体系
- ✅ **自动 L1 检查** - 禁用词、禁用标点、空泛工具名自动扫描
- ✅ **质检报告** - 每篇文章生成详细质检报告
- ✅ **严格模式** - L1 不通过可阻断发布流程

## When to Use This Skill

**MUST use when:**
- Creating complete blog articles from research to publishing
- Generating daily AI reports or news briefings
- Managing end-to-end content creation workflow
- Coordinating research, writing, image generation, and publishing sub-tasks

**Trigger phrases:**
- "create article"
- "generate daily report"
- "run content pipeline"
- "write and publish"
- "content creation workflow"
- Scheduled content tasks

## Quick Start

```bash
# Full pipeline with QA: research → write → QA → image → publish
~/.openclaw/skills/cypher-content-pipeline/scripts/run.sh \
  --type research \
  --topic "LangGraph Best Practices" \
  --publish true

# Skip QA (not recommended)
~/.openclaw/skills/cypher-content-pipeline/scripts/run.sh \
  --type research \
  --topic "Topic" \
  --skip-qa

# Strict mode - L1 must pass
~/.openclaw/skills/cypher-content-pipeline/scripts/run.sh \
  --type research \
  --topic "Topic" \
  --strict-qa
```

## Core Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Topic Selection & Research                        │
│  └── cypher-research-assistant                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 2: Article Writing                                   │
│  └── Generate content with style guidelines                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  🆕 Phase 2.5: Four-Layer QA (NEW)                          │
│  └── L1: 硬性规则 (Auto)                                    │
│  └── L2: 风格一致性 (Pattern)                               │
│  └── L3: 内容质量 (Deep)                                    │
│  └── L4: 活人感终审 (Human)                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Cover Generation                                  │
│  └── cypher-image-pipeline                                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Phase 4: Publish & Archive                                 │
│  └── cypher-publish-pipeline                                │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Topic Selection & Research

Use `cypher-research-assistant` skill:
- Multi-source aggregation (ducksearch/web_fetch/RSS)
- Deduplication filtering
- Structured data organization

**Research modes:**

| Mode | Depth | Time | Use Case |
|------|-------|------|----------|
| Quick | Low | 2-5 min | Daily reports |
| Standard | Medium | 10-15 min | Regular articles |
| Deep | High | 30+ min | Research papers |

## Phase 2: Article Writing

Select writing mode based on content type:

| Type | Depth | Length | Frequency |
|------|-------|--------|-----------|
| Research | High | 4000-8000 chars | 2/day |
| Briefing | Medium | 2000-3000 chars | 1/day |
| Quick | Low | 1000-2000 chars | On demand |

### Writing Guidelines (for AI generation)

**风格要求:**
1. **开头**: 从具体事件切入，避免"在当今AI时代"
2. **口语化**: 使用"坦率的讲"、"我当时就愣住了"等表达
3. **节奏**: 长短句交替，适当一句一段
4. **禁用**: 冒号、破折号、双引号、"说白了"
5. **人称**: 多用第一人称"我觉得"、"我的感受"

## Phase 2.5: Four-Layer QA ⭐ NEW

自动运行质检，检查文章质量。

### L1: 硬性规则 (Auto)
```bash
python3 ~/.openclaw/skills/cypher-writing-qa/scripts/qa_check.py \
  --file /tmp/article.md \
  --fail-on-l1
```

**检查项:**
- 禁用词（"说白了"、"本质上"等）
- 禁用标点（冒号、破折号、双引号）
- 空泛工具名（"AI工具" → "Claude Code"）

### L2: 风格一致性 (Pattern)
- 开头检查（具体事件切入）
- 节奏检查（长短句交替）
- 口语化程度（≥8个口语词组）

### L3: 内容质量 (Deep)
- 观点支撑（具体案例）
- 知识输出方式（随手掏出）
- 文化升维（连接更大参照）

### L4: 活人感终审 (Human)
需人工检查:
- 温度感（体感记忆 vs 知识描述）
- 独特性（作者独特视角）
- 姿态（朋友聊天 vs 导师讲课）
- 心流（读完全程无断点）

### QA Decision Matrix

| L1 | L2 | L3 | Action |
|----|----|----|--------|
| ❌ | - | - | 必须修复 L1 后才能发布 |
| ✅ | ❌ | - | 警告，可继续（建议改进） |
| ✅ | ✅ | ❌ | 警告，可继续（建议改进） |
| ✅ | ✅ | ✅ | 通过，进入 L4 人工检查 |

## Phase 3: Cover Generation

Use `cypher-image-pipeline` skill:

**Workflow:**
1. Get base image (Picsum or user-provided)
2. Content matching check
3. Sharp conversion to WebP
4. PicGo upload to Qiniu
5. Return cover URL

## Phase 4: Publish & Archive

Use `cypher-publish-pipeline` skill:
1. Save to `chen-blog/source/_posts/`
2. Git commit & push
3. Vercel auto-deployment
4. Archive to `chen-notes/06-内容创作/04-已发布/`

## Examples

### Example 1: Research Article with QA
```bash
# Create research article with full QA
~/.openclaw/skills/cypher-content-pipeline/scripts/run.sh \
  --type research \
  --topic "LangGraph Agent Planning Best Practices" \
  --research-depth deep \
  --length long \
  --strict-qa \
  --publish true \
  --archive true

# Output:
# ✅ Researched: 15 sources
# ✅ Generated: 5000 chars article
# ✅ QA Report: L1✅ L2✅ L3✅ (See: /tmp/qa-report.md)
# ✅ Cover: https://qiniu.aichanning.cn/...
# ✅ Published: https://blog.aichanning.cn/...
```

### Example 2: Daily AI Report
```bash
# Generate AI daily report
~/.openclaw/skills/cypher-content-pipeline/scripts/run.sh \
  --type daily \
  --topic "AI Daily Report $(date +%Y-%m-%d)" \
  --research-sources "OpenAI Blog,TechCrunch AI,Ars Technica" \
  --max-items 10 \
  --publish true
```

### Example 3: Manual QA Check
```bash
# Run QA on existing article
python3 ~/.openclaw/skills/cypher-writing-qa/scripts/qa_check.py \
  --file ~/drafts/my-article.md \
  --output ~/drafts/qa-report.md

# View report
cat ~/drafts/qa-report.md
```

## QA Report Example

```markdown
## 写作质检报告

### L1 硬性规则 [✅]
- L1-禁用词: ✅
- L1-禁用标点: ✅
- L1-空泛工具名: ✅

### L2 风格一致性 [✅]
- L2-口语化: ✅ (12个口语词组)
- L2-情绪表达: ✅ (发现 。。。 和 ？？？)
- L2-结构节奏: ✅

### L3 内容质量 [⚠️]
- L3-内容质量: ⚠️
  - 可能缺少具体案例支撑

### L4 活人感终审 [需人工检查]
- [ ] 温度感
- [ ] 独特性
- [ ] 姿态
- [ ] 心流

**总评**: 2.5/3 层通过
**建议**: 补充具体案例后可发布
```

## Quality Checklist

Before publishing, verify:
- [ ] Article has complete frontmatter (title, date, tags, categories, permalink, cover)
- [ ] L1 QA passed (no banned words/punctuation)
- [ ] L2 QA passed (casual phrases, rhythm)
- [ ] L3 QA warnings addressed
- [ ] L4 manual check completed
- [ ] Cover image URL is valid and accessible
- [ ] Permalink is set correctly
- [ ] Content is deduplicated (not similar to recent 3 days)
- [ ] QA report saved

## Configuration

### QA Settings
```bash
# Strict mode - fail if L1 doesn't pass
--strict-qa

# Skip QA (not recommended for production)
--skip-qa

# Custom QA config
--qa-config ~/.openclaw/config/writing-qa.yaml
```

### Default Settings
```bash
# Content pipeline defaults
CONTENT_TYPE="research"
RESEARCH_DEPTH="standard"
MAX_ITEMS=10
PUBLISH=true
ARCHIVE=true
QA_ENABLED=true
QA_STRICT=false
```

## Error Handling

| Phase | Error | Fallback |
|-------|-------|----------|
| Research | Source unavailable | Switch to alternative source |
| Writing | Generation failed | Use template-based fallback |
| **QA** | **L1 failed** | **Block publish, return for fix** |
| QA | L2/L3 warning | Log warning, continue (if not strict) |
| Image | Picsum failed | Use default placeholder |
| Publish | Git conflict | Auto-stash, pull, retry |

## Sub-Skill Reference

```python
# Research phase
read skill:cypher-research-assistant/SKILL.md

# QA phase ⭐ NEW
read skill:cypher-writing-qa/SKILL.md
python3 ~/.openclaw/skills/cypher-writing-qa/scripts/qa_check.py

# Image phase
read skill:cypher-image-pipeline/SKILL.md

# Publish phase
read skill:cypher-publish-pipeline/SKILL.md
```

## Integration

### With cypher-auto-writer
```bash
# Autonomous writing uses content pipeline internally
read skill:cypher-auto-writer/SKILL.md
# → Calls content-pipeline with QA enabled
```

### With cypher-distribute-pipeline
```bash
# After publishing, distribute to platforms
source ~/.openclaw/skills/cypher-content-pipeline/scripts/run.sh
result=$(run_pipeline --topic "AI News" --publish true)

# Extract URL and distribute
url=$(echo $result | jq -r '.blogUrl')
source ~/.openclaw/skills/cypher-distribute-pipeline/scripts/distribute.sh
push_article "AI News" "$url" "Summary..." "discord,telegram"
```

## File Naming Convention

| Type | Pattern | Example |
|------|---------|---------|
| Research | `YYYY-MM-DD-topic.md` | `2026-03-11-langgraph-guide.md` |
| Daily | `YYYY-MM-DD-ai-daily.md` | `2026-03-11-ai-daily.md` |
| QA Report | `YYYY-MM-DD-topic-qa.md` | `2026-03-11-langgraph-guide-qa.md` |

## References

- QA system inspired by: 数字生命卡兹克 (khazix-writer)
- Source: https://github.com/KKKKhazix/khazix-skills
