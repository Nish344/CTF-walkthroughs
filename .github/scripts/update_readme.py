#!/usr/bin/env python3
import re
import os
from pathlib import Path
from collections import defaultdict, OrderedDict

try:
    import yaml
except ImportError:
    yaml = None  # GitHub Action will install pyyaml

# --------- SETTINGS: edit these to your liking ----------
REPO_TITLE = "🛡️ Cybersecurity Lab Reports & CTF Write-ups"
REPO_BLURB = (
    "Welcome to my collection of **Vulnerability Assessment and Penetration Testing (VAPT) reports** "
    "and **CTF walkthroughs**. This repository documents my journey in ethical hacking, penetration "
    "testing, and cybersecurity challenges."
)

CONNECT_GITHUB = "https://github.com/Nish344"
CONNECT_LINKEDIN = "https://linkedin.com/in/nishanth-antony-b60110289"

# Top-level folders you want included (auto-detected if empty)
INCLUDE_TOP_LEVEL = []  # e.g., ["TryHackMe", "PicoCTF", "CTFlearn"]
# Folders to ignore globally
IGNORE_DIRS = {".git", ".github", ".vscode", "__pycache__", "assets", "images", "img"}

DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2}
# --------------------------------------------------------


def read_file_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def parse_front_matter(text: str):
    """
    Returns dict of front matter and the text without FM.
    Supports '---' YAML front matter at the very beginning of the file.
    """
    fm_re = r"^\s*---\s*\n(.*?)\n---\s*\n?"
    m = re.match(fm_re, text, flags=re.DOTALL)
    if not m:
        return {}, text
    fm_block = m.group(1)
    rest = text[m.end():]
    if yaml:
        try:
            data = yaml.safe_load(fm_block) or {}
        except Exception:
            data = {}
    else:
        # Minimal fallback: try to parse simple key: value pairs
        data = {}
        for line in fm_block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data, rest


def first_h1(text: str) -> str | None:
    for line in text.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return None


def guess_platform_and_difficulty(md_path: Path):
    parts = md_path.parts
    # Guess Platform from first-level directory
    platform = parts[0] if len(parts) > 1 else None
    # Guess Difficulty from second-level directory (e.g., TryHackMe/Easy/Challenge.md)
    difficulty = parts[1] if len(parts) > 2 else None

    # Normalize difficulty
    if difficulty:
        d = difficulty.lower()
        if "easy" in d:
            difficulty = "Easy"
        elif "medium" in d:
            difficulty = "Medium"
        elif "hard" in d:
            difficulty = "Hard"
        else:
            difficulty = None
    return platform, difficulty


def scan_repo(repo_root: Path):
    # Determine platforms to include
    top_dirs = [p for p in repo_root.iterdir() if p.is_dir() and p.name not in IGNORE_DIRS]
    if INCLUDE_TOP_LEVEL:
        top_dirs = [repo_root / d for d in INCLUDE_TOP_LEVEL if (repo_root / d).is_dir()]

    entries = []  # each: dict
    tree = defaultdict(list)  # platform -> list of (relpath, is_dir)

    for top in top_dirs:
        platform = top.name
        for p in top.rglob("*.md"):
            if p.name.lower() == "readme.md":
                continue
            rel = p.relative_to(repo_root)
            text = read_file_text(p)
            fm, body = parse_front_matter(text)

            chall_name = fm.get("Challenge") or first_h1(body) or p.stem.replace("_", " ").replace("-", " ")
            plat = fm.get("Platform") or platform
            diff = fm.get("Difficulty")
            if not diff:
                _, guess_diff = guess_platform_and_difficulty(rel)
                diff = guess_diff or "Unspecified"

            points = fm.get("Points", "")
            skills = fm.get("Skills", [])
            if isinstance(skills, str):
                # allow comma-separated string
                skills = [s.strip() for s in skills.split(",") if s.strip()]

            entries.append({
                "challenge": chall_name,
                "platform": plat,
                "difficulty": diff,
                "points": points,
                "skills": skills,
                "relpath": str(rel).replace("\\", "/"),
            })

        # Build tree view (files + dirs, 2 levels deep for readability)
        for item in sorted(top.iterdir()):
            if item.name in IGNORE_DIRS:
                continue
            if item.is_dir():
                tree[platform].append((str(item.relative_to(repo_root)).replace("\\", "/"), True))
                for sub in sorted(item.iterdir()):
                    if sub.is_dir():
                        tree[platform].append((str(sub.relative_to(repo_root)).replace("\\", "/"), True))
                    elif sub.suffix.lower() == ".md":
                        tree[platform].append((str(sub.relative_to(repo_root)).replace("\\", "/"), False))
            elif item.suffix.lower() == ".md":
                tree[platform].append((str(item.relative_to(repo_root)).replace("\\", "/"), False))

    return entries, tree


def build_tree_markdown(tree):
    out = []
    for platform in sorted(tree.keys()):
        out.append(f"### 📁 {platform}")
        last_dir = None
        for rel, is_dir in tree[platform]:
            depth = rel.count("/")  # simple indent
            indent = "    " * depth
            name = rel.split("/")[-1]
            if is_dir:
                out.append(f"{indent}- **{name}/**")
                last_dir = rel
            else:
                out.append(f"{indent}- [{name}]({rel})")
        out.append("")  # blank line
    return "\n".join(out).strip()


def build_table(entries):
    # Sort by Platform, Difficulty, then Challenge
    def sort_key(e):
        return (
            e["platform"] or "",
            DIFFICULTY_ORDER.get(e["difficulty"], 99),
            e["challenge"].lower(),
        )

    entries_sorted = sorted(entries, key=sort_key)

    head = "| Challenge | Platform | Difficulty | Skills | Link |\n|---|---|---|---|---|"
    rows = []
    for e in entries_sorted:
        skills = ", ".join(e["skills"]) if e["skills"] else "—"
        link = f"[Open]({e['relpath']})"
        rows.append(f"| {e['challenge']} | {e['platform']} | {e['difficulty']} | {skills} | {link} |")

    return "\n".join([head] + rows) if rows else "_No write-ups found yet._"


def aggregate_skills(entries):
    skills = set()
    for e in entries:
        for s in e["skills"]:
            if s.strip():
                skills.add(s.strip())
    if not skills:
        return "_(Will auto-populate as you add front-matter `Skills` to write-ups)_"
    return "- " + "\n- ".join(sorted(skills, key=lambda x: x.lower()))


def build_readme(repo_root: Path):
    entries, tree = scan_repo(repo_root)

    tree_md = build_tree_markdown(tree)
    table_md = build_table(entries)
    skills_md = aggregate_skills(entries)

    readme = f"""# {REPO_TITLE}

{REPO_BLURB}

Each report includes:
- **Reconnaissance steps** (how I scanned and identified services)
- **Exploitation process** (how I gained access)
- **Proof of Concept (PoC)**
- **Privilege escalation techniques**
- **Mitigation recommendations**
- **Lessons learned & skills practiced**

---

## 📂 Repository Structure
{tree_md if tree_md else "_(Folders and write-ups will appear here automatically.)_"}

---

## ✅ Completed Write-ups
{table_md}

---

## 🎯 Skills Covered So Far
{skills_md}

---

## 📌 About This Repository
I actively solve CTF challenges from:
- [TryHackMe](https://tryhackme.com)
- [PicoCTF](https://picoctf.org)
- [CTFlearn](https://ctflearn.com)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

This repository is both my **learning archive** and **portfolio**. Each write-up is prepared with a focus on clarity so beginners can follow along.

---

## 📬 Connect with Me
- **GitHub:** {CONNECT_GITHUB}
- **LinkedIn:** {CONNECT_LINKEDIN}
"""
    return readme


def main():
    repo_root = Path(".").resolve()
    readme = build_readme(repo_root)
    Path("README.md").write_text(readme, encoding="utf-8")
    print("README.md regenerated.")


if __name__ == "__main__":
    main()
