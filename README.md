# 🕵️‍♂️ Discord 🔍 OSINT Tool

## 🏴‍☠️ Created by Rocky Singh

This **⚔️ Ultimate OSINT Tool** is designed to extract **🔎 Open Source Intelligence (OSINT)** from **🎮 Discord user profiles** and their **🔗 linked accounts**. It utilizes the **💻 Discord API** and multiple other platform APIs to **collect, analyze, and organize** intelligence. Ideal for **cybersecurity professionals, ethical hackers, and digital investigators**. 🕶️💀

---

## 🔥 Features
✅ **Retrieve Detailed Discord User Profiles** 🏴‍☠️  
✅ **Extract Emails 📧, Usernames & Account IDs** 🔎  
✅ **Scan Connected Accounts 🔗 on:**
   - 🎮 **Steam**
   - 🐙 **GitHub**
   - ▶️ **YouTube**
   - 🎵 **Spotify**
   - 🐦 **Twitter**
   - 🎥 **Twitch**
   - 🎮 **PlayStation**
✅ **Find Mutual Servers 🏴‍☠️**  
✅ **Export Data 📂 in TXT & JSON formats**  
✅ **Dark Terminal Output 🌑 for Hacker Aesthetic**  
✅ **Automated Email Extraction & Verification** ✉️  
✅ **Support for Proxy Requests & Custom Headers** 🛡️  

---

## 🛠️ Installation
### 📌 Requirements
- 🐍 Python 3.7+
- 📦 Required Python modules:
  ```sh
  pip install -r requirements.txt
  ```
- A valid **🔐 Discord API token**

---

## 🚀 Usage
Run the 🛠️ with the following command:

```sh
python discord_osint.py <discord_user_id> -t <your_token> [options]
```

### ⚙️ Arguments:
- `discord_user_id` - The **🎮 Discord ID** of the user to investigate (**Required**)

### 🔧 Options:
- `-t, --token` - **🔑 Discord API Token** (**Required**)
- `-f, --file` - **💾 Output file name** (default: `data`)
- `-o` - **📂 Output format** (`json` or `txt`)
- `-p, --proxy` - **🌐 Use a proxy (optional)**
- `--verbose` - **📢 Display detailed logs**

### 📖 Example:
```sh
python discord_osint.py 123456789 -t "your_discord_token_here" -o output.txt --verbose
```

---

## 📊 Hacker-Style Output Example
```
███████████████████████████████████████████████████
█                                                 █
█  🔍 SCANNING DISCORD ID: 123456789012345678      █
█                                                 █
███████████████████████████████████████████████████

💀 **Username:** DarkHunter#1337  
💀 **Display Name:** ShadowHacker  
💀 **Bio:** "Hacking the system since '99"  
💀 **Gmail Found:** ✉️ darkhunter1337@gmail.com  
💀 **Phone:** 📱 +1 555-****-789  
💀 **Badges:** 🏆 Nitro, 🔥 Early Supporter  
💀 **Mutual Servers:** 🏴‍☠️ HackerSpace, 🏴‍☠️ CyberWarriors  
💀 **Connected Accounts:**  
    🎮 Steam: steamcommunity.com/id/darkhunter  
    🐱 GitHub: github.com/dark1337  
    🎥 Twitch: twitch.tv/dark_hacker  
```

---

## 📡 Future Updates 🚀
- **🌍 Advanced IP Geolocation**
- **📥 Dark Web Email Leak Lookup**
- **📡 Deep Discord Server Intelligence**
- **💀 More Social Media Integrations**
- **🚀 Automated OSINT Reporting**

👨‍💻 **Contributions & Suggestions Welcome!**

---

💀 **For ethical use only! 🕶️ Stay Anonymous. Stay Safe.** 💀
