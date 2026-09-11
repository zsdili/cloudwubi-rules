#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rule_verify.py - CloudWubi 五笔规则库自动校验器（CI 核心程序）

作用：在 CI 中自动校验 PR 提交的五笔编码规则文件，
非法条目直接拦截，保证去中心化共建的规则库质量。

校验规则：
1. 编码格式：1~4 位小写字母 a~y（86五笔标准，z 保留）
2. 每行至少 1 个汉字
3. 汉字必须是合法 Unicode 中文字符（CJK 统一表意文字区）
4. 编码不重复（同编码追加为重码候选，需人工确认）
5. 注释行（#开头）和空行跳过

用法：
    python3 rule_verify.py <规则文件> [更多规则文件...]
    返回码 0 = 全部通过；非 0 = 有非法条目
"""

import re
import sys
import unicodedata

# 编码正则：1~4 位 a~y
CODE_RE = re.compile(r"^[a-y]{1,4}$")

# CJK 统一表意文字区段
CJK_RANGES = [
    (0x4E00, 0x9FFF),   # 基本区
    (0x3400, 0x4DBF),   # 扩展A
    (0x20000, 0x2A6DF), # 扩展B
    (0x2A700, 0x2B73F), # 扩展C
    (0x2B740, 0x2B81F), # 扩展D
    (0x2B820, 0x2CEAF), # 扩展E
    (0x2CEB0, 0x2EBEF), # 扩展F
    (0x30000, 0x3134F), # 扩展G
]


def is_cjk_char(ch: str) -> bool:
    """判断字符是否属于 CJK 统一表意文字。"""
    cp = ord(ch)
    for lo, hi in CJK_RANGES:
        if lo <= cp <= hi:
            return True
    return False


def verify_file(path: str) -> tuple:
    """校验单个规则文件，返回 (是否通过, 错误列表, 有效条目数)。"""
    errors = []
    seen_codes = set()
    valid_count = 0

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (IOError, UnicodeDecodeError) as e:
        return False, [f"无法读取文件 {path}: {e}"], 0

    for line_no, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            errors.append(f"第{line_no}行: 格式错误，应为 '编码 汉字...'（当前: {line}）")
            continue

        code = parts[0]
        chars = parts[1:]

        # 1) 编码格式校验
        if not CODE_RE.match(code):
            errors.append(f"第{line_no}行: 编码 '{code}' 非法，需 1~4 位小写字母 a~y")

        # 2) 汉字校验
        for word in chars:
            for ch in word:
                if not is_cjk_char(ch):
                    errors.append(f"第{line_no}行: 字符 '{ch}' 不是 CJK 汉字")

        # 3) 编码重复校验
        if code in seen_codes:
            errors.append(f"第{line_no}行: 编码 '{code}' 重复定义（重码请合并到同一行）")
        else:
            seen_codes.add(code)

        if not errors or not any(f"第{line_no}行" in e for e in errors):
            valid_count += 1

    return (len(errors) == 0), errors, valid_count


def main():
    if len(sys.argv) < 2:
        print("用法: python3 rule_verify.py <规则文件> [更多文件...]")
        sys.exit(2)

    all_pass = True
    total_valid = 0

    for path in sys.argv[1:]:
        ok, errors, valid_count = verify_file(path)
        total_valid += valid_count
        print(f"\n=== 文件: {path} ===")
        print(f"有效条目: {valid_count}")

        if ok:
            print("✅ 校验通过")
        else:
            all_pass = False
            print(f"❌ 发现 {len(errors)} 个问题:")
            for err in errors[:50]:  # 最多显示前50个错误
                print(f"   {err}")
            if len(errors) > 50:
                print(f"   ... 还有 {len(errors) - 50} 个错误未显示")

    print(f"\n=== 总计: {total_valid} 条有效规则 ===")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
