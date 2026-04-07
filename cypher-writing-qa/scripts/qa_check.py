#!/usr/bin/env python3
"""
Cypher Writing QA - 四层写作质检系统
检查文章质量，去除 AI 味
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class QAResult:
    level: str
    passed: bool
    issues: List[str]
    suggestions: List[str]

class WritingQA:
    # L1: 禁用词
    BANNED_WORDS = {
        "说白了": ["坦率的讲", "其实就是"],
        "意味着什么": ["那结果会怎样呢", "所以呢"],
        "这意味着": ["那结果会怎样呢", "所以呢"],
        "本质上": ["说到底", "其实"],
        "换句话说": ["你想想看", "也就是说"],
        "不可否认": [None],  # 直接删除
        "综上所述": [None],
        "总的来说": [None],
        "值得注意的是": [None],
        "不难发现": [None],
        "让我们来看看": [None],
        "接下来让我们": [None],
        "在当今": [None],
        "随着": [None],
    }
    
    # L1: 禁用标点
    BANNED_PUNCTUATION = [":", "——", '"', '"']
    
    # L1: 空泛工具名模式
    VAGUE_TOOLS = ["AI工具", "某个模型", "相关技术", "AI产品"]
    
    # L2: 推荐口语化词组
    CASUAL_PHRASES = [
        "坦率的讲", "说真的", "我是真的觉得", "怎么说呢", "其实吧",
        "你想想看", "我跟你说", "我有时候觉得", "我一直觉得",
        "说实话我也不确定", "我自己也还在摸索", "当时就愣住了",
        "想想就觉得兴奋", "回到", "顺着上面的"
    ]
    
    # L2: 情绪标点
    EMOTION_PUNCTUATION = ["。。。", "？？？", "= =", "尼玛", "卧槽"]
    
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.results: List[QAResult] = []
    
    def check_l1_banned_words(self, content: str) -> QAResult:
        """L1: 禁用词检查"""
        issues = []
        suggestions = []
        
        for word, replacements in self.BANNED_WORDS.items():
            matches = list(re.finditer(re.escape(word), content))
            if matches:
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    context = content[max(0, match.start()-20):min(len(content), match.end()+20)]
                    issues.append(f"行{line_num}: 发现禁用词 '{word}'")
                    issues.append(f"  上下文: ...{context}...")
                    if replacements and replacements[0]:
                        suggestions.append(f"'{word}' → '{replacements[0]}'")
                    else:
                        suggestions.append(f"'{word}' → 建议删除")
        
        return QAResult(
            level="L1-禁用词",
            passed=len(issues) == 0,
            issues=issues,
            suggestions=suggestions
        )
    
    def check_l1_banned_punctuation(self, content: str) -> QAResult:
        """L1: 禁用标点检查"""
        issues = []
        suggestions = []
        
        for punct in self.BANNED_PUNCTUATION:
            matches = list(re.finditer(re.escape(punct), content))
            if matches:
                for match in matches[:5]:  # 最多显示5处
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(f"行{line_num}: 发现禁用标点 '{punct}'")
                if len(matches) > 5:
                    issues.append(f"  ... 还有 {len(matches)-5} 处")
                suggestions.append(f"'{punct}' → 用逗号或句号替代")
        
        return QAResult(
            level="L1-禁用标点",
            passed=len(issues) == 0,
            issues=issues,
            suggestions=suggestions
        )
    
    def check_l1_vague_tools(self, content: str) -> QAResult:
        """L1: 空泛工具名检查"""
        issues = []
        suggestions = []
        
        for vague in self.VAGUE_TOOLS:
            matches = list(re.finditer(re.escape(vague), content))
            if matches:
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(f"行{line_num}: 发现空泛工具名 '{vague}'")
                suggestions.append(f"'{vague}' → 使用具体工具名如 'Claude Code'、'GPT-4'")
        
        return QAResult(
            level="L1-空泛工具名",
            passed=len(issues) == 0,
            issues=issues,
            suggestions=suggestions
        )
    
    def check_l2_casual_phrases(self, content: str) -> QAResult:
        """L2: 口语化词组检查"""
        found_phrases = []
        
        for phrase in self.CASUAL_PHRASES:
            if phrase in content:
                found_phrases.append(phrase)
        
        issues = []
        suggestions = []
        
        if len(found_phrases) < 5:
            issues.append(f"口语化词组仅 {len(found_phrases)} 个，建议至少 8-10 个")
            suggestions.append("增加口语化表达，如：坦率的讲、说真的、我当时就愣住了")
        
        return QAResult(
            level="L2-口语化",
            passed=len(found_phrases) >= 5,
            issues=issues,
            suggestions=suggestions + [f"已发现: {', '.join(found_phrases[:5])}{'...' if len(found_phrases) > 5 else ''}"]
        )
    
    def check_l2_emotion_punctuation(self, content: str) -> QAResult:
        """L2: 情绪标点检查"""
        found_emotions = []
        
        for punct in self.EMOTION_PUNCTUATION:
            if punct in content:
                found_emotions.append(punct)
        
        issues = []
        suggestions = []
        
        if not found_emotions:
            issues.append("未使用情绪标点，文章可能偏书面")
            suggestions.append("适当使用 。。。？？？= = 等表达情绪")
        
        return QAResult(
            level="L2-情绪表达",
            passed=len(found_emotions) > 0,
            issues=issues,
            suggestions=suggestions + [f"已发现: {', '.join(found_emotions)}"]
        )
    
    def check_l2_structure(self, content: str) -> QAResult:
        """L2: 结构节奏检查"""
        issues = []
        suggestions = []
        
        # 检查段落长度
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        long_paragraphs = [p for p in paragraphs if len(p) > 200]
        
        if len(long_paragraphs) > len(paragraphs) * 0.5:
            issues.append(f"长段落占比过高 ({len(long_paragraphs)}/{len(paragraphs)})")
            suggestions.append("增加短段落，一句话一段可以增强节奏感")
        
        # 检查是否有独立短句
        short_lines = [p for p in content.split('\n') if 3 < len(p.strip()) < 20]
        if len(short_lines) < 3:
            issues.append("独立短句较少，缺乏'断裂'效果")
            suggestions.append("增加短句独立成段，如：'黑暗森林。' '大时代啊。'")
        
        return QAResult(
            level="L2-结构节奏",
            passed=len(issues) <= 1,
            issues=issues,
            suggestions=suggestions
        )
    
    def check_l3_content(self, content: str) -> QAResult:
        """L3: 内容质量粗略检查"""
        issues = []
        suggestions = []
        
        # 检查是否有具体案例（通过"比如"、"就像"等词）
        example_markers = ["比如", "就像", "举个例子", "像", "我在"]
        has_examples = any(marker in content for marker in example_markers)
        
        if not has_examples:
            issues.append("可能缺少具体案例支撑")
            suggestions.append("增加具体场景或例子，如'就像我上周遇到的...'")
        
        # 检查是否有第一人称
        first_person = ["我", "我们", "我的"]
        has_first_person = any(p in content for p in first_person)
        
        if not has_first_person:
            issues.append("缺少第一人称视角")
            suggestions.append("增加个人视角，如'我觉得'、'我的感受是'")
        
        return QAResult(
            level="L3-内容质量",
            passed=len(issues) <= 1,
            issues=issues,
            suggestions=suggestions
        )
    
    def run_all_checks(self, content: str) -> List[QAResult]:
        """运行所有检查"""
        self.results = [
            self.check_l1_banned_words(content),
            self.check_l1_banned_punctuation(content),
            self.check_l1_vague_tools(content),
            self.check_l2_casual_phrases(content),
            self.check_l2_emotion_punctuation(content),
            self.check_l2_structure(content),
            self.check_l3_content(content),
        ]
        return self.results
    
    def generate_report(self) -> str:
        """生成质检报告"""
        lines = ["## 写作质检报告\n"]
        
        l1_results = [r for r in self.results if r.level.startswith("L1")]
        l2_results = [r for r in self.results if r.level.startswith("L2")]
        l3_results = [r for r in self.results if r.level.startswith("L3")]
        
        # L1 汇总
        l1_passed = all(r.passed for r in l1_results)
        lines.append(f"### L1 硬性规则 [{'✅' if l1_passed else '❌'}]\n")
        for r in l1_results:
            status = "✅" if r.passed else "❌"
            lines.append(f"- {r.level}: {status}")
            if r.issues:
                for issue in r.issues[:3]:  # 最多显示3个
                    lines.append(f"  - {issue}")
        lines.append("")
        
        # L2 汇总
        l2_passed = sum(r.passed for r in l2_results) >= 2  # 至少2/3通过
        lines.append(f"### L2 风格一致性 [{'✅' if l2_passed else '❌'}]\n")
        for r in l2_results:
            status = "✅" if r.passed else "⚠️"
            lines.append(f"- {r.level}: {status}")
            if r.suggestions and not r.passed:
                lines.append(f"  - {r.suggestions[0]}")
        lines.append("")
        
        # L3 汇总
        l3_passed = all(r.passed for r in l3_results)
        lines.append(f"### L3 内容质量 [{'✅' if l3_passed else '⚠️'}]\n")
        for r in l3_results:
            status = "✅" if r.passed else "⚠️"
            lines.append(f"- {r.level}: {status}")
            if r.issues:
                lines.append(f"  - {r.issues[0]}")
        lines.append("")
        
        # L4 提示
        lines.append("### L4 活人感终审 [需人工检查]\n")
        lines.append("- [ ] 温度感：情绪是体感记忆而非知识描述")
        lines.append("- [ ] 独特性：有作者独特视角")
        lines.append("- [ ] 姿态：像朋友聊天而非导师讲课")
        lines.append("- [ ] 心流：读完全程无断点")
        lines.append("")
        
        # 总评
        total_passed = l1_passed + l2_passed + l3_passed
        lines.append(f"**总评**: {total_passed}/3 层通过")
        
        if not l1_passed:
            lines.append("**⚠️ 建议**: L1 必须修复后再发布")
        elif not l2_passed:
            lines.append("**💡 建议**: 增加口语化表达，改善节奏")
        elif not l3_passed:
            lines.append("**💡 建议**: 补充具体案例和个人视角")
        else:
            lines.append("**✅ 文章质量良好，可进行 L4 人工终审**")
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Cypher Writing QA - 写作质检工具")
    parser.add_argument("--file", "-f", required=True, help="文章文件路径")
    parser.add_argument("--output", "-o", help="报告输出路径")
    parser.add_argument("--strict-mode", action="store_true", help="严格模式")
    parser.add_argument("--fail-on-l1", action="store_true", help="L1不通过返回错误码")
    
    args = parser.parse_args()
    
    # 读取文件
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"错误: 文件不存在 {args.file}", file=sys.stderr)
        sys.exit(1)
    
    content = file_path.read_text(encoding="utf-8")
    
    # 运行质检
    qa = WritingQA(strict_mode=args.strict_mode)
    qa.run_all_checks(content)
    report = qa.generate_report()
    
    # 输出报告
    print(report)
    
    # 保存报告
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(report, encoding="utf-8")
        print(f"\n报告已保存: {output_path}")
    
    # 检查 L1 是否通过
    l1_results = [r for r in qa.results if r.level.startswith("L1")]
    l1_passed = all(r.passed for r in l1_results)
    
    if args.fail_on_l1 and not l1_passed:
        sys.exit(2)  # L1 检查失败
    
    sys.exit(0 if all(r.passed for r in qa.results[:3]) else 1)


if __name__ == "__main__":
    main()
