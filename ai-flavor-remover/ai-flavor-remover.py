#!/usr/bin/env python3
"""
AI Flavor Remover - 通用版
让 AI 生成的文字读起来像人写的
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 默认配置
DEFAULT_CONFIG = {
    "mode": "medium",
    "domain": "general",
    "customReplacements": {},
    "preservePatterns": []
}

# AI 味词汇库
AI_WORDS = {
    "值得注意的是": ["", "有意思的是", "你会发现", "特别的是"],
    "不难发现": ["明眼人都看得出", "稍微留意就会发现", "其实不难发现"],
    "基于以上分析": ["说到底", "往深里说", "说白了", "所以"],
    "综上所述": ["总结一下", "说到底", "所以", "一言以蔽之"],
    "从某种程度上说": ["某种程度上", "一定程度上", "可以说"],
    "显而易见": ["很显然", "明摆着", "不用说也明白", "显而易见的是"],
    "换句话说": ["说白了", "也就是说", "换言之", "换句话说就是"],
    "因此": ["所以", "这样一来", "结果就是", "于是"],
    "此外": ["还有", "另外", "再说", "除此之外"],
    "然而": ["但是", "不过", "问题是", "然而现实是"],
    "首先": ["先来说说", "首先说说", "", "一开始"],
    "其次": ["再说", "另外", "还有一点", "其次要说的是"],
    "最后": ["最后说说", "说到底", "至于", "最后一点"],
}

# 机械句式检测
MECHANICAL_PATTERNS = [
    r"首先.*其次.*最后",  # 首先...其次...最后
    r"^[^，。！？]{30,}$",  # 超长无标点句
    r"（[一二三四五]）",  # （一）（二）（三）
]

# 领域风格提示
DOMAIN_PROMPTS = {
    "tech": """技术文章风格：
- 保留专业术语，但解释要接地气
- 用类比和比喻降低认知门槛
- 允许适度的"硬核"表达
- 保留代码块和技术细节
风格：精准、务实、有洞见、不炫技""",

    "essay": """随笔散文风格：
- 情感优先，逻辑次之
- 多用感官描写和场景还原
- 允许碎片化叙述
- 强调个人体验
风格：温度、细腻、留白、共鸣""",

    "business": """商业分析风格：
- 数据驱动，观点明确
- 用案例和故事包装抽象概念
- 结论前置，论证在后
- 适度使用行业术语
风格：洞察、锐利、有说服力""",

    "casual": """ casual 内容风格：
- 最大程度口语化
- 允许网络用语和表情
- 短句为主，节奏轻快
- 朋友聊天一样的平等视角
风格：轻松、好玩、不做作、有梗"""
}


class AIFlavorRemover:
    def __init__(self, config: Dict):
        self.config = config
        self.mode = config.get("mode", "medium")
        self.domain = config.get("domain", "general")
        self.custom_replacements = config.get("customReplacements", {})
        self.preserve_patterns = config.get("preservePatterns", [])
        
    def detect_ai_flavor(self, text: str) -> Dict:
        """检测文章中的 AI 味特征"""
        issues = {
            "high_freq_words": [],
            "mechanical_patterns": [],
            "suggestions": []
        }
        
        # 检测高频 AI 词
        for word in AI_WORDS.keys():
            count = text.count(word)
            if count > 0:
                issues["high_freq_words"].append(f"{word} ({count}次)")
        
        # 检测机械句式
        for pattern in MECHANICAL_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                issues["mechanical_patterns"].append(pattern)
        
        # 建议模式
        word_count = len(issues["high_freq_words"])
        if word_count > 5:
            issues["suggestions"].append("建议用 heavy 模式")
        elif word_count > 2:
            issues["suggestions"].append("建议用 medium 模式")
        else:
            issues["suggestions"].append("建议用 light 模式")
            
        return issues
    
    def remove_ai_flavor_light(self, text: str) -> str:
        """轻度润色：替换高频词，微调句式"""
        result = text
        
        # 替换高频 AI 词
        for word, replacements in AI_WORDS.items():
            if word in result:
                # 随机选择替换（第一个通常是最佳）
                replacement = replacements[0] if replacements[0] else replacements[1] if len(replacements) > 1 else ""
                result = result.replace(word, replacement)
        
        # 简单句式调整
        result = re.sub(r"首先，", "先来说说", result)
        result = re.sub(r"其次，", "再说", result)
        result = re.sub(r"最后，", "最后说说", result)
        
        return result
    
    def remove_ai_flavor_medium(self, text: str) -> str:
        """中度润色：light + 句式重组 + 情感注入"""
        result = self.remove_ai_flavor_light(text)
        
        # 打破均匀句式
        sentences = re.split(r'([。！？])', result)
        processed = []
        for i, sent in enumerate(sentences):
            if sent in [".", "!", "?", "。", "！", "？"]:
                processed.append(sent)
                continue
            # 随机插入口语化表达
            if i > 0 and i % 3 == 0 and len(sent) > 20:
                sent = self._add_casual_touch(sent)
            processed.append(sent)
        result = "".join(processed)
        
        # 增强连接
        result = re.sub(r"此外，", "还有，", result)
        result = re.sub(r"然而，", "但是，", result)
        result = re.sub(r"因此，", "所以，", result)
        
        return result
    
    def remove_ai_flavor_heavy(self, text: str) -> str:
        """重度润色：medium + 结构重组 + 领域风格"""
        result = self.remove_ai_flavor_medium(text)
        
        # 添加领域风格引导
        if self.domain in DOMAIN_PROMPTS:
            # 这里可以接入 LLM 进行深度重写
            # 目前做简单处理
            pass
        
        return result
    
    def _add_casual_touch(self, sentence: str) -> str:
        """为句子添加口语化触感"""
        prefixes = ["其实", "说实话", "说白了", "你会发现"]
        import random
        if random.random() < 0.3:  # 30% 概率添加
            prefix = random.choice(prefixes)
            return f"{prefix}，{sentence.lstrip()}"
        return sentence
    
    def process(self, text: str) -> str:
        """根据模式选择处理方式"""
        if self.mode == "light":
            return self.remove_ai_flavor_light(text)
        elif self.mode == "heavy":
            return self.remove_ai_flavor_heavy(text)
        else:  # medium (default)
            return self.remove_ai_flavor_medium(text)


def load_config(config_path: Optional[str] = None) -> Dict:
    """加载配置文件"""
    config = DEFAULT_CONFIG.copy()
    
    # 尝试加载用户配置
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            config.update(user_config)
    elif os.path.exists('.ai-flavor-remover.json'):
        with open('.ai-flavor-remover.json', 'r', encoding='utf-8') as f:
            user_config = json.load(f)
            config.update(user_config)
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description='AI Flavor Remover - 让 AI 生成的文字读起来像人写的'
    )
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('--mode', '-m', 
                       choices=['light', 'medium', 'heavy'],
                       default='medium',
                       help='润色模式 (默认: medium)')
    parser.add_argument('--domain', '-d',
                       choices=['tech', 'essay', 'business', 'casual', 'general'],
                       default='general',
                       help='文章领域 (默认: general)')
    parser.add_argument('--output', '-o',
                       help='输出路径 (默认: 覆盖原文件或添加 .polished 后缀)')
    parser.add_argument('--detect-only', action='store_true',
                       help='仅检测 AI 味，不润色')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    parser.add_argument('--batch', '-b', action='store_true',
                       help='批量处理目录')
    parser.add_argument('--config', '-c',
                       help='配置文件路径')
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    config['mode'] = args.mode
    config['domain'] = args.domain
    
    # 初始化处理器
    remover = AIFlavorRemover(config)
    
    # 处理输入
    input_path = Path(args.input)
    
    if args.batch or input_path.is_dir():
        # 批量处理
        files = list(input_path.glob('*.md')) + list(input_path.glob('*.txt'))
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if args.detect_only:
                issues = remover.detect_ai_flavor(content)
                print(f"\n[文件] {file.name}")
                print(f"  AI高频词: {len(issues['high_freq_words'])} 个")
                print(f"  建议: {issues['suggestions'][0]}")
            else:
                polished = remover.process(content)
                output_file = args.output / file.name if args.output else file.with_suffix('.polished.md')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(polished)
                print(f"已处理: {file.name} -> {output_file}")
    else:
        # 单文件处理
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if args.detect_only:
            issues = remover.detect_ai_flavor(content)
            print("\n[AI 味检测报告]")
            print(f"高频 AI 词 ({len(issues['high_freq_words'])} 个):")
            for word in issues['high_freq_words']:
                print(f"  - {word}")
            print(f"\n机械句式 ({len(issues['mechanical_patterns'])} 处)")
            print(f"\n建议: {issues['suggestions'][0]}")
        else:
            polished = remover.process(content)
            
            if args.verbose:
                issues = remover.detect_ai_flavor(content)
                print("\n[润色摘要]")
                print(f"- 检测到 AI 词: {len(issues['high_freq_words'])} 个")
                print(f"- 处理模式: {args.mode}")
                print(f"- 领域适配: {args.domain}")
                print("\n[润色后文章]\n")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(polished)
                print(f"已保存到: {args.output}")
            else:
                print(polished)


if __name__ == '__main__':
    main()
