#!/usr/bin/env python3
import os
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

# ---------------- SETTINGS ----------------
REPO_TITLE = "🛡️ Cybersecurity Lab Reports & CTF Write-ups"
REPO_BLURB = (
    "Welcome to my collection of **Vulnerability Assessment and Penetration Testing (VAPT) reports** "
    "and **CTF walkthroughs**. This repository documents my journey in ethical hacking, penetration "
    "testing, and cybersecurity challenges."
)

CONNECT_GITHUB = "https://github.com/Nish344"
CONNECT_LINKEDIN = "https://linkedin.com/in/nishanth-antony-b60110289"

INCLUDE_TOP_LEVEL = []
IGNORE_DIRS = {".git", ".github", ".vscode", "__pycache__", "assets", "images", "img"}
IGNORE_FILES = {"README.md"}

DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2}
# -------------------------------------------------------------

try:
    import yaml
except Exception:
    yaml = None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def parse_front_matter(text: str):
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n?", text, flags=re.DOTALL)
    if not m:
        return {}, text
    fm_block = m.group(1)
    rest = text[m.end():]
    data = {}
    if yaml:
        try:
            data = yaml.safe_load(fm_block) or {}
        except Exception:
            data = {}
    else:
        for line in fm_block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data, rest


def first_h1(text: str):
    for line in text.splitlines():
        if line.lstrip().startswith("# "):
            return line.lstrip()[2:].strip()
    return None


def guess_platform_and_difficulty(relpath: Path):
    parts = relpath.parts
    platform = parts[0] if len(parts) >= 1 else None
    difficulty = None
    if len(parts) >= 2:
        d = parts[1].lower()
        if "easy" in d:
            difficulty = "Easy"
        elif "medium" in d:
            difficulty = "Medium"
        elif "hard" in d:
            difficulty = "Hard"
    return platform, difficulty


def extract_skills_from_body(body: str):
    skills = set()
    heading = re.search(r"(?im)^(#{2,6})\s*skills(?:\s*(?:covered|demonstrated)?)?\s*$", body)
    if not heading:
        heading = re.search(r"(?im)^\*\*skills(?:\s*(?:covered|demonstrated)?)?\*\*\s*: ?\s*$", body)
    if not heading:
        return []
    start = heading.end()
    tail = body[start:]
    for line in tail.splitlines():
        if re.match(r"^\s*#{1,6}\s+", line):
            break
        m = re.match(r"^\s*[-*•]\s+(.*\S)\s*$", line)
        if m:
            skills.add(m.group(1).strip())
    return list(skills)


def should_include_dir(dir_path: Path) -> bool:
    for p in dir_path.rglob("*.md"):
        if p.name not in IGNORE_FILES:
            return True
    return False


def collect_entries_and_tree(repo_root: Path):
    if INCLUDE_TOP_LEVEL:
        top_dirs = [repo_root / d for d in INCLUDE_TOP_LEVEL if (repo_root / d).is_dir()]
    else:
        top_dirs = [
            p for p in repo_root.iterdir()
            if p.is_dir() and p.name not in IGNORE_DIRS and should_include_dir(p)
        ]

    def build_node(dir_path: Path):
        node = {"_files": [], "_dirs": {}}
        for child in sorted(dir_path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if child.name in IGNORE_DIRS:
                continue
            if child.is_dir():
                if should_include_dir(child):
                    node["_dirs"][child.name] = build_node(child)
            elif child.suffix.lower() == ".md" and child.name not in IGNORE_FILES:
                rel = child.relative_to(repo_root).as_posix()
                node["_files"].append((child.name, rel))
        return node

    tree = {}
    for top in sorted(top_dirs, key=lambda p: p.name.lower()):
        tree[top.name] = build_node(top)

    entries = []
    for platform_name, platform_node in tree.items():
        for md_path in (repo_root / platform_name).rglob("*.md"):
            if md_path.name in IGNORE_FILES:
                continue
            text = read_text(md_path)
            fm, body = parse_front_matter(text)

            challenge = fm.get("Challenge") or first_h1(body) or md_path.stem.replace("_", " ").replace("-", " ")
            platform = fm.get("Platform") or guess_platform_and_difficulty(md_path.relative_to(repo_root))[0] or platform_name
            difficulty = fm.get("Difficulty") or guess_platform_and_difficulty(md_path.relative_to(repo_root))[1] or "Unspecified"
            points = fm.get("Points", "")

            skills = fm.get("Skills")
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(",") if s.strip()]
            if not skills:
                skills = extract_skills_from_body(body)

            entries.append({
                "challenge": challenge,
                "platform": platform,
                "difficulty": difficulty,
                "points": points,
                "skills": skills or [],
                "relpath": md_path.relative_to(repo_root).as_posix(),
                "date": datetime.fromtimestamp(md_path.stat().st_mtime)
            })
    return entries, tree


def render_tree_md(tree: dict) -> str:
    lines = []
    def render_node(name: str, node: dict, depth: int):
        indent = "    " * depth
        for subdir, subnode in node.get("_dirs", {}).items():
            lines.append(f"{indent}- **{subdir}/**")
            render_node(subdir, subnode, depth + 1)
        for fname, rel in node.get("_files", []):
            lines.append(f"{indent}- [{fname}]({rel})")

    for platform in sorted(tree.keys(), key=lambda s: s.lower()):
        lines.append(f"### 📁 {platform}\n")
        render_node(platform, tree[platform], depth=0)
        lines.append("")
    return "\n".join(lines).strip() or "_(Folders and write-ups will appear here automatically.)_"


def build_table(entries: list) -> str:
    def sk(e):
        return (e["platform"].lower(), DIFFICULTY_ORDER.get(e["difficulty"], 99), e["challenge"].lower())
    entries_sorted = sorted(entries, key=sk)
    if not entries_sorted:
        return "_No write-ups found yet._"

    head = "| Challenge | Platform | Difficulty | Link |\n|---|---|---|---|"
    rows = []
    for e in entries_sorted:
        rows.append(f"| {e['challenge']} | {e['platform']} | {e['difficulty']} | [Open]({e['relpath']}) |")
    return "\n".join([head] + rows)


def aggregate_skills(entries: list) -> str:
    bag = set()
    for e in entries:
        for s in e["skills"]:
            s = s.strip()
            if s:
                bag.add(s)
    if not bag:
        return "_(Will auto-populate as you add `Skills` in front-matter or a `## Skills` section in write-ups.)_"
    out = "- " + "\n- ".join(sorted(bag, key=lambda x: x.lower()))
    return out

def generate_ctf_graphs(entries, outdir="assets"):
    os.makedirs(outdir, exist_ok=True)

    # Collect dates (use file creation date if you want)
    data = []
    for e in entries:
        # if you’re not storing dates in metadata, use today as fallback
        data.append({"date": e.get("date", datetime.today().date())})

    df = pd.DataFrame(data)

    # 🔑 Convert to datetime before resampling
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.set_index("date").resample("D").size().to_frame("count").fillna(0)

    # Plot heatmap-like calendar (weekly)
    pivot = df.reset_index()
    pivot["dow"] = pivot["date"].dt.dayofweek  # Monday=0
    pivot["week"] = pivot["date"].dt.isocalendar().week
    heatmap_data = pivot.pivot("dow", "week", "count")

    plt.figure(figsize=(12, 3))
    sns.heatmap(heatmap_data, cmap="Greens", cbar=False, linewidths=0.5)
    plt.title("CTF Solves Calendar Heatmap")
    plt.yticks([0,1,2,3,4,5,6], ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"], rotation=0)
    plt.tight_layout()
    plt.savefig(f"{outdir}/ctf_heatmap.svg")
    plt.close()



def build_readme(repo_root: Path) -> str:
    entries, tree = collect_entries_and_tree(repo_root)
    tree_md = render_tree_md(tree)
    table_md = build_table(entries)
    skills_md = aggregate_skills(entries)

    generate_ctf_graphs(entries)

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
{tree_md}

---

## ✅ Completed Write-ups
{table_md}

---

## 🎯 Skills Covered So Far
{skills_md}

---

## 📊 CTF Stats
![By Platform](assets/ctf_by_platform.svg)
![By Difficulty](assets/ctf_by_difficulty.svg)
![Heatmap](assets/ctf_heatmap.svg)

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
    md = build_readme(repo_root)
    Path("README.md").write_text(md, encoding="utf-8")
    print("README.md regenerated with graphs and heatmap.")


if __name__ == "__main__":
    main()
