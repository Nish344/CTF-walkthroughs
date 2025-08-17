#!/usr/bin/env python3
import os
import re
from pathlib import Path
from collections import defaultdict

# ---------------- SETTINGS (edit if you want) ----------------
REPO_TITLE = "🛡️ Cybersecurity Lab Reports & CTF Write-ups"
REPO_BLURB = (
    "Welcome to my collection of **Vulnerability Assessment and Penetration Testing (VAPT) reports** "
    "and **CTF walkthroughs**. This repository documents my journey in ethical hacking, penetration "
    "testing, and cybersecurity challenges."
)

CONNECT_GITHUB = "https://github.com/Nish344"
CONNECT_LINKEDIN = "https://linkedin.com/in/nishanth-antony-b60110289"

# Top-level folders to include; leave empty to auto-detect
INCLUDE_TOP_LEVEL = []  # e.g. ["TryHackMe", "PicoCTF", "CTFlearn"]

# Ignore sets
IGNORE_DIRS = {".git", ".github", ".vscode", "__pycache__", "assets", "images", "img"}
IGNORE_FILES = {"README.md"}

# Difficulty ordering for table sort
DIFFICULTY_ORDER = {"Easy": 0, "Medium": 1, "Hard": 2}
# -------------------------------------------------------------

# Optional dependency: PyYAML (the Action installs it). We degrade gracefully if missing.
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
    """
    Extract YAML front matter (--- ... ---) at the beginning of a file.
    Returns (data_dict, body_without_fm).
    """
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
        # Fallback parser: "Key: Value" lines only
        for line in fm_block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data, rest


def first_h1(text: str) -> str | None:
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
    """
    Heuristic: look for a section header containing 'Skills' and collect bullet points until the next header.
    Supports headings like:
      ## Skills
      ## Skills Covered
      ## Skills Demonstrated
    Bullets recognized: -, *, •
    """
    skills = set()
    # Find a 'skills' heading
    heading = re.search(r"(?im)^(#{2,6})\s*skills(?:\s*(?:covered|demonstrated)?)?\s*$", body)
    if not heading:
        # Also support bold label style: **Skills Demonstrated:** on its own line
        heading = re.search(r"(?im)^\*\*skills(?:\s*(?:covered|demonstrated)?)?\*\*\s*:?\s*$", body)
    if not heading:
        return []

    start = heading.end()
    # Slice lines after heading
    tail = body[start:]
    for line in tail.splitlines():
        if re.match(r"^\s*#{1,6}\s+", line):  # next heading reached
            break
        m = re.match(r"^\s*[-*•]\s+(.*\S)\s*$", line)
        if m:
            skills.add(m.group(1).strip())
    return list(skills)


def should_include_dir(dir_path: Path) -> bool:
    """
    Include this directory if it (recursively) contains at least one .md (excluding README.md).
    """
    for p in dir_path.rglob("*.md"):
        if p.name not in IGNORE_FILES:
            return True
    return False


def collect_entries_and_tree(repo_root: Path):
    """
    Scans repo for markdown write-ups and builds:
      - entries: list of write-ups with metadata for the table & skills
      - tree: nested dict structure for rendering the repo structure
    """
    # Determine top-level platforms
    if INCLUDE_TOP_LEVEL:
        top_dirs = [repo_root / d for d in INCLUDE_TOP_LEVEL if (repo_root / d).is_dir()]
    else:
        top_dirs = [
            p for p in repo_root.iterdir()
            if p.is_dir() and p.name not in IGNORE_DIRS and should_include_dir(p)
        ]

    # Build nested tree: { platform_name: node }, where node = {"_files":[(name, relpath)], "_dirs":{subdir: node}}
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

    # Collect entries for table & skills
    entries = []
    for platform_name, platform_node in tree.items():
        for md_path in (repo_root / platform_name).rglob("*.md"):
            if md_path.name in IGNORE_FILES:
                continue
            text = read_text(md_path)
            fm, body = parse_front_matter(text)

            # Basic fields
            challenge = fm.get("Challenge") or first_h1(body) or md_path.stem.replace("_", " ").replace("-", " ")
            platform = fm.get("Platform") or guess_platform_and_difficulty(md_path.relative_to(repo_root))[0] or platform_name
            difficulty = fm.get("Difficulty") or guess_platform_and_difficulty(md_path.relative_to(repo_root))[1] or "Unspecified"
            points = fm.get("Points", "")

            # Skills
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
            })
    return entries, tree


def render_tree_md(tree: dict) -> str:
    """
    Renders the nested tree as a Markdown bullet list with folder icons & clickable file links.
    """
    lines = []

    def render_node(name: str, node: dict, depth: int):
        indent = "    " * depth
        # Render directories first
        for subdir, subnode in node.get("_dirs", {}).items():
            lines.append(f"{indent}- **{subdir}/**")
            render_node(subdir, subnode, depth + 1)
        # Then files
        for fname, rel in node.get("_files", []):
            lines.append(f"{indent}- [{fname}]({rel})")

    # Top-level sections per platform in alpha order
    for platform in sorted(tree.keys(), key=lambda s: s.lower()):
        lines.append(f"### 📁 {platform}\n")
        render_node(platform, tree[platform], depth=0)
        lines.append("")  # blank line
    return "\n".join(lines).strip() or "_(Folders and write-ups will appear here automatically.)_"


def build_table(entries: list) -> str:
    def sk(e):
        return (
            e["platform"].lower(),
            DIFFICULTY_ORDER.get(e["difficulty"], 99),
            e["challenge"].lower()
        )
    entries_sorted = sorted(entries, key=sk)
    if not entries_sorted:
        return "_No write-ups found yet._"

    head = "| Challenge | Platform | Difficulty | Skills | Link |\n|---|---|---|---|---|"
    rows = []
    for e in entries_sorted:
        skills = ", ".join(e["skills"]) if e["skills"] else "—"
        rows.append(f"| {e['challenge']} | {e['platform']} | {e['difficulty']} | {skills} | [Open]({e['relpath']}) |")
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


def build_readme(repo_root: Path) -> str:
    entries, tree = collect_entries_and_tree(repo_root)
    tree_md = render_tree_md(tree)
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
{tree_md}

---

## ✅ Completed Write-ups
{table_md}

---

## 🎯 Skills Covered So Far
 Reconnaissance: `nmap`, `gobuster`, `dirb`, `enum4linux` 
 Exploitation: `FTP login`, `SQLi`, `command injection`, `SSRF`, `path traversal` 
 Password Attacks: `hydra`, `john` 
 Post-Exploitation: `Privilege escalation`, `sudo misconfigurations` 
 Tools: `nmap`, `ftp`, `hydra`, `ssh`, `sudo`, `tar`, `sqlmap`, `burpsuite`

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
    print("README.md regenerated.")


if __name__ == "__main__":
    main()
