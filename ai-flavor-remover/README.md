# AI Flavor Remover CLI 使用指南

## 安装

```bash
# 添加到 PATH
chmod +x ai-flavor-remover.py
sudo ln -s $(pwd)/ai-flavor-remover.py /usr/local/bin/ai-flavor-remover

# 或直接运行
python3 ai-flavor-remover.py <文章.md>
```

## 基础用法

```bash
# 默认中度润色
ai-flavor-remover article.md

# 轻度润色（仅替换高频词）
ai-flavor-remover --mode=light article.md

# 重度润色（深度改写）
ai-flavor-remover --mode=heavy --domain=essay article.md

# 输出到新文件
ai-flavor-remover article.md --output=article-polished.md
```

## 检测 AI 味

```bash
# 只检测不润色
ai-flavor-remover article.md --detect-only

# 详细报告
ai-flavor-remover article.md --detect-only --verbose
```

## 批量处理

```bash
# 处理整个目录
ai-flavor-remover ./posts/ --batch

# 批量并指定输出目录
ai-flavor-remover ./raw/ --batch --output=./polished/
```

## 领域适配

```bash
# 技术文章（保留术语，解释接地气）
ai-flavor-remover --domain=tech docs.md

# 随笔散文（情感优先，细节丰富）
ai-flavor-remover --domain=essay blog.md

# 商业分析（数据驱动，观点明确）
ai-flavor-remover --domain=business report.md

# 轻松 casual（口语化，有梗）
ai-flavor-remover --domain=casual social.md
```

## 配置文件

创建 `.ai-flavor-remover.json`：

```json
{
  "mode": "medium",
  "domain": "tech",
  "customReplacements": {
    "系统": "平台",
    "用户": "你"
  },
  "preservePatterns": ["API", "JSON"]
}
```

## 使用示例

### 示例 1：技术博客润色

```bash
# 先用检测模式看看问题
ai-flavor-remover openclaw-guide.md --detect-only

# 输出：
# [AI 味检测报告]
# 高频 AI 词 (5 个):
#   - 值得注意的是 (2次)
#   - 不难发现 (1次)
#   - 综上所述 (1次)
# 建议: 建议用 medium 模式

# 然后用 medium 模式润色
ai-flavor-remover --mode=medium --domain=tech openclaw-guide.md --output=openclaw-guide-polished.md
```

### 示例 2：批量处理博客文章

```bash
# 处理所有文章
ai-flavor-remover ./source/_posts/ --batch --mode=light

# 生成的文件：
# ./source/_posts/article1.polished.md
# ./source/_posts/article2.polished.md
```

### 示例 3：CI/CD 集成

在 GitHub Actions 中使用：

```yaml
name: Polish Articles
on:
  push:
    paths:
      - '_posts/**'

jobs:
  polish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup AI Flavor Remover
        run: |
          pip install ai-flavor-remover
          
      - name: Polish new articles
        run: |
          ai-flavor-remover ./_posts/ --batch --mode=medium --domain=tech
          
      - name: Commit changes
        run: |
          git add .
          git commit -m "chore: 润色新文章"
          git push
```

## 最佳实践

1. **分级处理**
   - 初稿：heavy 模式彻底重写
   - 修订：medium 模式精细调整
   - 终稿：light 模式局部打磨

2. **先检测后润色**
   ```bash
   ai-flavor-remover article.md --detect-only
   # 根据建议选择合适的模式
   ```

3. **保持领域一致**
   同一系列文章使用相同的 domain 设置

4. **人工复核**
   重度润色后务必通读，确保没有偏离原意

## 常见问题

**Q: 润色后的文章还能保留 markdown 格式吗？**
A: 可以，工具会保留原有的 markdown 结构和代码块。

**Q: 如何保留某些专业术语不被替换？**
A: 在配置文件的 `preservePatterns` 中添加需要保留的词汇。

**Q: 能否自定义替换词库？**
A: 可以，在配置文件的 `customReplacements` 中定义你的替换规则。

**Q: 润色后文章变长了正常吗？**
A: 正常，特别是 medium/heavy 模式会添加过渡句和解释，使文章更易读。
