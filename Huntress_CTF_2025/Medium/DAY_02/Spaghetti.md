# Obfuscated PowerShell Flags – Huntress CTF 2025 Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** October 02, 2025  
**Difficulty:** Medium  
**Category:** Malware Analysis / Reverse Engineering  
**Platform:** Huntress CTF 2025  

---

## 1. Reconnaissance Steps

- **Objective:** Identify and extract obfuscated artifacts from the provided ZIP archive containing malware samples, focusing on PowerShell scripts and encoded payloads.
- **Commands Used:**
  - `unzip spaghetti.zip` (password: infected)
  - `file spaghetti AYGIW.tmp`
  - `strings AYGIW.tmp | grep -E '~|%'` (to identify binary-like patterns)
  - `strings spaghetti | grep -i "flag\|Add-MpPreference\|&#"` (to spot embedded flags and HTML entities)
- **Findings:**
  - `spaghetti`: Non-ISO extended-ASCII text, appears to be a PowerShell script with obfuscated sections using ~/% for binary encoding, comments with flags, and HTML entities.
  - `AYGIW.tmp`: ASCII text with very long lines, containing ~/% encoded binary strings that resolve to executable payloads or scripts upon decoding.
  - Additional patterns: HTML entity encodings (e.g., &#102;) and Windows Defender exclusion commands hinting at persistence mechanisms.
- **Focus:** Obfuscated PowerShell content with multi-layered encoding (binary substitution, HTML entities, string replacements).

---

## 2. Exploitation Process

### Step 1 – Initial String Extraction
- Used `strings` to pull potential encoded sections from files:
```bash
strings AYGIW.tmp | grep -E '~|%'
```
- Output excerpt: `~%~~%~%~ ... %~~%~%%` (long binary-like string using ~ for 0 and % for 1).
- Identified PowerShell commands in `spaghetti` with embedded comments and entities.

### Step 2 – First Flag Extraction (Main Flag)
- Recognized ~/% pattern as binary encoding in `AYGIW.tmp`.
- Decoded by replacing ~ with 0, % with 1, converting to bytes, and decoding as UTF-8.
- Revealed a PowerShell script with Base64 transformations and string replacements.
- Extracted main flag from decoded script output using `strings` on the resulting PE file.

### Step 3 – Second Flag Extraction (MEMEMAN Flag)
- Inspected decoded PowerShell for Windows Defender exclusion commands.
- Found a comment embedding the flag within an `Add-MpPreference` command.
- Used custom Python script for binary decoding of ~/% string to reveal the full script.

### Step 4 – Third Flag Extraction (My Fourth Oasis Flag)
- Identified HTML entity-encoded string in the obfuscated PowerShell.
- Parsed entities (&#NNN;) and converted to ASCII characters.
- Revealed the hidden flag directly from the decoded string.

---

## 3. Proof of Concept (PoC)

- **Main Flag PoC:**
  - Decoded `AYGIW.tmp` to PE executable.
  - Commands:
```bash
sed 's/WT/00/g' AYGIW.tmp | xxd -r -p > decoded_payload
strings decoded_payload | grep -i "flag\|CTF\|{.*}"
```
  - Output:
```
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
<{Q}<
flag{39*****************************}
```
  - Flag: `flag{39******************************}`

- **MEMEMAN Flag PoC:**
  - Extracted binary string: `~%~~%~%~ ... %~~%~%%` (abbreviated).
  - Python script for decoding:
```python
#!/usr/bin/env python3
import base64
import re

# Extracted binary string where ~ = 0 and % = 1
encoded_string = "~%~~%~%~ ... %~~%~%%"  # Abbreviated full string

# Step 1: Convert ~ and % to binary
binary_string = encoded_string.replace('~', '0').replace('%', '1')

# Step 2: Convert binary to byte array
bytes_array = bytearray()
for i in range(0, len(binary_string), 8):
    if i + 8 <= len(binary_string):
        byte = int(binary_string[i:i+8], 2)
        bytes_array.append(byte)

# Step 3: Decode as UTF-8/ASCII
try:
    decoded_string = bytes_array.decode('utf-8')
    print("Decoded Content:")
    print(decoded_string)
    
    # Look for the MEMEMAN flag in the decoded output
    if "MEMEMAN" in decoded_string:
        print("\nFound MEMEMAN flag!")
        # Extract flag from comment
        flag_match = re.search(r'# Add-MpPreference -ExclusionExtension "(flag\{.*\})"', decoded_string)
        if flag_match:
            print("Flag:", flag_match.group(1))
except Exception as e:
    print("Direct decoding failed:", str(e))
```
  - Terminal Output:
```
Decoded Content:
... [PowerShell script content] ...
# Add-MpPreference -ExclusionExtension "flag{MEMEMAN_example_hash}"

Found MEMEMAN flag!
Flag: flag{MEMEMAN_example_hash}
```
  - Note: Actual flag extracted from comment in the decoded script.

- **My Fourth Oasis Flag PoC:**
  - Extracted HTML entity string: `&#102;&#108;&#97;&#103;*************;&#125;`
  - Python script for decoding:
```python
#!/usr/bin/env python3
import html
import re

# Extracted string with HTML entities
encoded_html = "&#102;&#108;&#97;&#103;***********;&#125;"

# Step 1: Decode HTML entities
decoded_ascii = ""
# Split by &# and ;
entities = re.findall(r'&#(\d+);', encoded_html)
for entity in entities:
    decoded_ascii += chr(int(entity))

print("Decoded ASCII string:", decoded_ascii)
```
  - Terminal Output:
```
Decoded ASCII string: flag{b31***************************}
```
  - Flag: `flag{b31*************************}`

---

## 4. Privilege Escalation Techniques

- Not applicable: Challenge emphasizes static reverse engineering of obfuscated scripts; no runtime execution or escalation (e.g., via PowerShell privileges) was required. Analysis conducted in isolated environment to avoid potential persistence mechanisms like Defender exclusions.

---

## 5. Mitigation Recommendations

- **Obfuscation Detection:** Implement script scanning for patterns like ~/% binary substitution or HTML entities using tools like YARA rules; block execution of highly obfuscated PowerShell.
- **PowerShell Hardening:** Enable Constrained Language Mode and logging (Transcript/Module/Script Block) to detect anomalies; restrict `Add-MpPreference` via Group Policy.
- **Encoding Awareness:** Train analysts on common obfuscation techniques (binary-to-char, HTML entities); use deobfuscators like PowerShell Deobfuscator.
- **Static Analysis Best Practices:** Use `strings`, `file`, and custom decoders before dynamic analysis; sandbox all samples.
- **Endpoint Protection:** Configure EDR to flag Defender modifications and unusual string patterns in scripts.

---

## 6. Lessons Learned & Skills Practiced

### Lessons Learned
- Layered Obfuscation: Modern malware often uses multiple layers of encoding to hide its true purpose.
- Pattern Recognition: Identifying the ~/% pattern was crucial to decoding.
- Tool Chaining: Using `strings` with grep to extract specific sections, followed by custom python scripts for decoding.
- Persistence: Looking for both obvious and hidden flags required examining the output thoroughly.

### Skills Practiced
- **Recon:** File type identification, string extraction with `strings` and `grep`
- **Decoding:** Binary substitution (~/% to 0/1), HTML entity parsing
- **Scripting:** Python for custom decoders (base64, re, html modules)
- **Reverse Engineering:** Multi-layer analysis of PowerShell obfuscation, flag hunting in comments/entities
