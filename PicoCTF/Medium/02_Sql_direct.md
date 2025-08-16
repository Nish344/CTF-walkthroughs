# 🛡️ PicoCTF Lab Walkthrough – SQL Direct

## 📌 Challenge Info
- **Category**: Web Exploitation  
- **Points**: 300  
- **Difficulty**: Medium  
- **Challenge Link**: [SQL Direct on PicoCTF](https://play.picoctf.org/practice/challenge/181)

---

## 📝 Challenge Description
> Connect directly to a PostgreSQL database with given credentials and retrieve the flag.

---

## 🔍 Initial Recon
**Objective:** Use `psql` to extract data.  
- **Service**: PostgreSQL on `saturn.picoctf.net:59980`  
- **Credentials**: user `postgres`, password `postgres`  
- **Files provided**: None  

---

## 🛠️ Tools & Commands Used
| Tool / Command | Purpose |
|----------------|---------|
| `psql` | Connect to PostgreSQL |
| `\dt` | List database tables |
| `SELECT` | Retrieve flag |

---

## 🧠 Step-by-Step Solution
1. **Connect to DB**
   ```bash
   psql -h saturn.picoctf.net -p 59980 -U postgres pico
Entered password: postgres.

List Tables
```bash
\dt
```
→ Found flags table.

Retrieve Data
```mysql
SELECT * FROM flags;
```
→ Flag displayed.

## 🧾 Flag
```text
picoCTF{direct_db_access_success}
```
## 📚 Learning Outcomes
Importance of DB hardening.

Using psql to enumerate data.

## 🛡️ Skills Learnt
PostgreSQL CLI basics

## 🔗 References
psql Docs
