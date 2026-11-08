#!/usr/bin/env python3
"""Offline, additive Vault bootstrap, bounded keyword search and file checks."""
import argparse
import json
import os
from pathlib import Path
import re
import sys

FOLDERS = ("00-收件箱", "10-来源", "20-知识卡", "30-主题", "40-输出", "90-模板", "99-系统", "附件")
FILES = {
    "开始这里.md": """# 我的个人知识库

从 [[30-主题/个人知识地图]] 开始。

收件箱 → 保留来源 → 提炼知识卡 → 连接主题 → 引用问答。
把资料放进 00-收件箱；原始资料归入 10-来源；一个问题一张知识卡。
AI 回答必须读到原文并标明来源；没有资料就记录待补充。
""",
    "30-主题/个人知识地图.md": """# 个人知识地图

## 示例（不是业务证据）
- [[10-来源/演示-知识库说明]]

## 我的主题
在这里链接你的来源和知识卡。
""",
    "10-来源/演示-知识库说明.md": """---
type: demo
source: skill-bundled-example
---
# 演示资料：知识库说明

这是演示笔记，不是真实业务资料。
资料可存为本地 Markdown；AI 的模型请求是否本地执行取决于宿主与模型设置。
""",
    "90-模板/来源模板.md": """# 来源标题

- 来源 URL / 原始文件：
- 收录日期：
- 处理方式（原文/抽取/OCR）：

## 正文

## 不确定处
""",
    "90-模板/知识卡模板.md": """# 一个明确的问题

## 结论

## 依据

## 适用范围

## 来源
填写指向已存在来源笔记的双链。

## 我的推断
与原文结论分开记录。
""",
    "99-系统/搭建记录.md": """# 搭建记录

- 当前阶段：仅创建文件结构
- Obsidian 界面：未验证
- 真实资料导入：未验证
- 引用问答：未验证
- 可选 RAG：未配置
- 下一步：在 Obsidian 打开此文件夹，导入第一篇授权资料

## 执行记录
后续追加实际环境、路径、测试与待办；保留历史，不记录密钥。
""",
}


def emit(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def root_path(value, must_exist=False):
    path = Path(value).expanduser().absolute()
    # Resolve system aliases (/var -> /private/var on macOS); reject a linked Vault itself.
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        raise ValueError("Vault 本身为符号链接或 junction，请改用真实路径")
    path = path.resolve()
    if path == Path(path.anchor):
        raise ValueError("请选择独立的 Vault 文件夹，不能使用磁盘根目录")
    if path.exists() and not path.is_dir():
        raise ValueError("Vault 路径已存在且不是文件夹")
    if must_exist and not path.is_dir():
        raise ValueError("Vault 尚不存在，请先 init")
    return path


def safe_target(root, relative):
    target = root / relative
    for node in (target, *target.parents):
        if node == root:
            break
        if node.is_symlink() or getattr(node, "is_junction", lambda: False)():
            raise ValueError("拒绝读写符号链接或 junction: " + relative)
    return target


def init_vault(args):
    root = root_path(args.vault)
    # Preflight every target before any writes, including same-name directories.
    for name in FOLDERS:
        target = safe_target(root, name)
        if target.exists() and not target.is_dir():
            raise ValueError("目标目录被文件占用: " + name)
    for name in FILES:
        target = safe_target(root, name)
        if target.exists() and not target.is_file():
            raise ValueError("目标笔记被目录占用: " + name)
    planned = [name for name in FILES if not (root / name).exists()]
    kept = [name for name in FILES if (root / name).exists()]
    created = []
    if args.apply:
        root.mkdir(parents=True, exist_ok=True)
        for name in FOLDERS:
            (root / name).mkdir(exist_ok=True)
        for name in planned:
            # Exclusive creation protects pre-existing notes even on repeated runs.
            try:
                with safe_target(root, name).open("x", encoding="utf-8", newline="\n") as out:
                    out.write(FILES[name])
                created.append(name)
            except FileExistsError:
                kept.append(name)
    emit({"vault": str(root), "mode": "apply" if args.apply else "dry-run", "planned": planned,
          "created": created, "preserved": kept, "gui_verified": False})


def markdown_files(root):
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and
                         not (Path(directory) / d).is_symlink() and
                         not getattr(Path(directory) / d, "is_junction", lambda: False)())
        for name in sorted(files):
            path = Path(directory) / name
            if name.lower().endswith(".md") and not path.is_symlink():
                yield path


def read_note(path):
    if path.stat().st_size > 2_000_000:
        raise ValueError("文件超过2MB，请拆分或使用宿主文件搜索")
    return path.read_text(encoding="utf-8-sig").splitlines()


def doctor(args):
    root = root_path(args.vault, must_exist=True)
    issues, notes = [], []
    for name in FOLDERS:
        try:
            if not safe_target(root, name).is_dir():
                issues.append("缺少起步目录: " + name)
        except ValueError as error:
            issues.append(str(error))
    for path in markdown_files(root):
        relative = path.relative_to(root).as_posix()
        try:
            lines = read_note(path)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append(relative + ": " + str(error))
            continue
        if not any(line.strip() for line in lines):
            issues.append("空笔记: " + relative)
        notes.append(relative)
    if not notes:
        issues.append("未找到 Markdown 笔记")
    emit({"vault": str(root), "markdown_count": len(notes), "issues": issues,
          "passed": not issues, "scope": "starter-file-structure-only", "gui_verified": False,
          "note": "已有库可沿用其他目录；此检查不证明引用正确、双链可点或AI问答可用"})
    return 1 if issues else 0


def query_terms(query):
    # Keep the full query plus ASCII words and Chinese bigrams (no tokenizer dependency).
    query = query.casefold().strip()
    terms = set(re.findall(r"[a-z0-9_-]+", query))
    for phrase in re.findall(r"[\u3400-\u9fff]+", query):
        terms.update(phrase[i:i + 2] for i in range(max(1, len(phrase) - 1)))
    if query:
        terms.add(query)
    return sorted(terms)


def search(args):
    root = root_path(args.vault, must_exist=True)
    terms = query_terms(args.query)
    if not terms:
        raise ValueError("查询词不能为空")
    found, skipped = [], []
    for path in markdown_files(root):
        rel = path.relative_to(root).as_posix()
        # Do not let templates or demo/system notes masquerade as source evidence.
        if rel.split("/")[0] in ("90-模板", "99-系统") or path.name.startswith("演示-"):
            continue
        try:
            lines = read_note(path)
        except (OSError, UnicodeError, ValueError) as error:
            skipped.append({"file": rel, "reason": str(error)})
            continue
        matches = [(sum(term in line.casefold() for term in terms), i) for i, line in enumerate(lines)]
        score, index = max(matches, default=(0, 0))
        if score:
            start, end = max(0, index - 2), min(len(lines), index + 4)
            found.append({"file": rel, "score": score, "line": index + 1,
                          "excerpt": [{"line": i + 1, "text": lines[i]} for i in range(start, end)]})
    found.sort(key=lambda result: (-result["score"], result["file"]))
    emit({"vault": str(root), "query": args.query, "method": "keyword-not-semantic",
          "results": found[:args.limit], "skipped": skipped,
          "note": "命中片段是检索候选，回答前读原文；无命中不代表事实不存在"})


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "doctor", "search"):
        command = sub.add_parser(name)
        command.add_argument("--vault", required=True)
        if name == "init":
            command.add_argument("--apply", action="store_true", help="write missing files; default is dry-run")
        if name == "search":
            command.add_argument("--query", required=True)
            command.add_argument("--limit", type=int, choices=range(1, 21), default=5)
    args = parser.parse_args()
    try:
        return {"init": init_vault, "doctor": doctor, "search": search}[args.command](args) or 0
    except (OSError, ValueError) as error:
        emit({"error": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
