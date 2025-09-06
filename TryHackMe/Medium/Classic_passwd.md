# Vulnerability Assessment and Penetration Testing (VAPT) Report  - Classic-passwd

**Prepared by:** Nishanth Antony  
**Date:** September 6, 2025  
**Difficulty:** Medium  
**Category:** Reverse Engineering  
**Platform:** TryHackMe (THM)  


## Overview

The provided binary `Challenge_1609966715991.Challenge` was a classic **reverse engineering / binary exploitation challenge**. The program prompted for a username, performed an internal comparison against a hardcoded value, and upon success revealed a flag in the format `THM{...}`.

By using dynamic analysis with **`ltrace`**, I was able to observe the internal library calls at runtime, discover the hidden hardcoded username, and successfully retrieve the flag.

---

## Reconnaissance

1. **File Preparation**
   The binary was renamed and made executable:

   ```bash
   mv Challenge_1609966715991.Challenge Challenge.Challenge
   chmod +x Challenge.Challenge
   ```

2. **Initial Execution**
   Running the program directly:

   ```bash
   ./Challenge.Challenge
   Insert your username: test
   Authentication Error
   ```

   * Any arbitrary input resulted in an **Authentication Error**.
   * This indicated the program had a hardcoded check against a specific value.

---

## Exploitation Methodology

### Why `ltrace`?

* `ltrace` intercepts **dynamic library calls** made by the binary during execution.
* Many programs use C standard library functions such as `strcmp`, `strcpy`, and `printf`.
* By tracing these calls, we can observe **what input is compared against** without needing to reverse engineer the assembly code.
* This makes `ltrace` an efficient first tool for password-checker style binaries.

---

### Observations with `ltrace`

#### Run with incorrect username (`vincida`):

```bash
ltrace ./Challenge.Challenge
```

Output (key parts):

```
printf("Insert your username: ")               
__isoc99_scanf(...)
strcpy(0x7ffceaf90280, "vincida")
strcmp("vincida", "AGB6js5d9dkG7") = 53
puts("\nAuthentication Error")
```

* **Key finding**: The binary compared our input `"vincida"` with a hidden hardcoded string `"AGB6js5d9dkG7"`.
* Since they did not match, the program printed **Authentication Error**.

---

#### Run with correct username (`AGB6js5d9dkG7`):

```
strcmp("AGB6js5d9dkG7", "AGB6js5d9dkG7") = 0
puts("\nWelcome")
printf("THM{%d%d}", 6523512, 8496)
```

* Strings matched → authentication succeeded.
* Program printed:

  ```
  Welcome
  THM{65235128496}
  ```

---

## Proof of Concept (PoC)

### Steps to Reproduce

1. Run `ltrace` on the binary:

   ```bash
   ltrace ./Challenge.Challenge
   ```

   * Observe the hardcoded username `"AGB6js5d9dkG7"`.

2. Provide the discovered username:

   ```bash
   ./Challenge.Challenge
   Insert your username: AGB6js5d9dkG7
   ```

   * Output:

     ```
     Welcome
     THM{65235128496}
     ```

### Flag

```
THM{65235128496}
```

---

## Technical Breakdown

* **`printf`** → Displayed the prompt.
* **`scanf`** → Accepted user input.
* **`strcpy`** → Copied input into a buffer.
* **`strcmp`** → Compared input with hardcoded string (`AGB6js5d9dkG7`).
* **`puts`** → Printed Authentication Error or Welcome.
* **`printf("THM{%d%d}", 6523512, 8496)`** → Generated the flag by formatting two integers together.

---

## Mitigation Recommendations

From a security standpoint:

1. **Avoid hardcoding secrets in binaries**.

   * Anyone can extract them using `ltrace`, `strings`, or disassembly.
   * Instead, validate credentials against an external secure source (e.g., database, config file with encryption).

2. **Obfuscation is not security**.

   * Even if obfuscation is applied, determined attackers can still reverse engineer the logic.

3. **Use proper authentication mechanisms**.

   * Implement hashed password checks instead of direct `strcmp` with plaintext.
   * Store sensitive data securely and never expose secrets in compiled code.

---

## Lessons Learned & Skills Practiced

* **Dynamic binary analysis with `ltrace`** to observe runtime behavior.
* Understanding how **standard library calls (`strcmp`) reveal hidden data**.
* Efficient exploitation without full reverse engineering.
* Reinforcing the principle that **static secrets in executables are insecure**.

---

## Final Notes

This challenge demonstrated how a seemingly opaque binary can be broken down with simple runtime tracing. Instead of brute force or guessing, using the right tool (`ltrace`) exposed the exact secret, allowing direct exploitation and flag retrieval.

✅ Challenge solved with flag: **THM{65235128496}**

---
