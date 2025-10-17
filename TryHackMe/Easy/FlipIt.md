# 🟩Flip It!! – Try Hack Me (THM) Walkthrough Report  

**Prepared by:** Nishanth Antony  
**Date:** August 12, 2025  
**Difficulty:** Medium  
**Category:** Cryptography / CBC Bit-Flipping Attack  
**Platform:** Try Hack Me (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify how the server handles authentication.
- **Connection Command:**
nc 10.201.63.180 1337

text
- **Observation:**
- Server prompts for username & password.
- Encrypts data with AES-CBC and **leaks** ciphertext.
- Auth success if decrypted input contains `"admin&password=sUp3rPaSs1"`.

---

## 2. Exploitation Process

1. **Test Inputs**  
 - Tried injection payloads → discovered banned chars (`/*`, `--`, `%0b`), but irrelevant since attack focuses on ciphertext, not plaintext input.

2. **Craft Input for Minimal Change**  
 - Used username: `bdmin` and password: `sUp3rPaSs1`.
 - Leaked ciphertext corresponds to:
   ```
   access_username=bdmin&password=sUp3rPaSs1
   ```
 - Only needed to flip `b` → `a` in `bdmin` to get `admin`.

3. **CBC Bit-Flipping Attack**  
 - Found XOR delta: `0x62 ^ 0x61 = 0x03`.
 - Modified corresponding byte in **IV** using XOR with `0x03`.
 - Submitted modified ciphertext.

---

## 3. Proof of Concept (PoC)

- After flipping the bit, the server decrypted my modified ciphertext, saw:
admin&password=sUp3rPaSs1

text
- Returned success message with **Flag**:
THM{FliP_DaT_B1t_oR_G3t_Fl1pP3d}

text

---

## 4. Privilege Escalation

- The cryptographic flaw itself acted as the “escalation” — escalating from normal user input to forged admin credentials **without knowing the key**.

---

## 5. Mitigation Recommendations

- **Use authenticated encryption**: AES-GCM or AES-CBC + HMAC.
- Always **verify integrity before decryption**.
- Don’t rely on **substring matching** for authentication logic.
- Avoid leaking raw ciphertext to the client.

---

## 6. Lessons Learned

- AES-CBC without integrity protection is vulnerable to bit-flipping.
- Even with random key/IV, ciphertext malleability can be abused if returned to the attacker.
- Small plaintext changes (1 byte) can be safely and predictably induced.

---

## 7. Skills Practiced

- Cryptanalysis of CBC mode.
- Bitwise XOR operations for targeted character changes.
- Reverse-engineering a custom crypto protocol.
- Using Python for ciphertext manipulation.

---
If you want, I can also bundle Light + Flip It!! into one combined .md file with a table of contents so you have a single GitHub upload for day-24 challenges.
Do you want me to prepare that combined file? That will keep your repo cleaner.
