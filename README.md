# 🕵️‍♂️ Discord 🔍 OSINT Tool

## 🏆 Created by Rocky Singh

This 🛠️ is designed to gather **🔎 Open Source Intelligence (OSINT)** from 🎮 Discord user profiles and their connected 🔗 accounts. It leverages the **💻 Discord API** and various other platform APIs to collect 📊 and organize 🗂️ information.

---

## 🌟 Features
- Retrieve **🎮 Discord user profile** ℹ️
- Gather 📥 data from connected accounts:
  - 🎮 **Steam**
  - 🐙 **GitHub**
  - ▶️ **YouTube**
  - 🎵 **Spotify**
  - 🐦 **Twitter**
  - 🎥 **Twitch**
  - 🎮 **PlayStation**
- Extract **📧 emails & 🔗 links** from user bios and connected accounts
- Collect **👤 usernames, 🤝 friends lists & 🗃️ miscellaneous** info
- Export data in **📄 TXT & 📂 JSON** formats

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
python discord_osint.py <discord_user_id> [options]
```

### ⚙️ Arguments:
- `discord_user_id` - The **🎮 Discord ID** of the user to scrape (📌 Required)

### 🔧 Options:
- `-f, --file` - The **💾 output file name** (default: `data`)
- `-t, --token` - The **🔑 Discord token** for authentication
- `-o` - The **📂 output format** (`.json` or `.txt`)

### 📖 Example:
```sh
python discord_osint.py 123456789 -o output.txt -t "your_discord_token_here"
```

---

## 📊 Output
The 🛠️ generates a structured 📜 output containing:
- **🔗 Connected accounts**
- **👤 Usernames**
- **📧 Emails**
- **🤝 Friends**
- **🔗 Links**
- **📂 Miscellaneous information**

### 📑 Example JSON Output:
```json
███████████████████████████████████████████████████
█                                                 █
█  🔍 Scanning Discord ID: 123456789012345678      █
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
💀 **Profile Picture:** [Click Here](https://cdn.discordapp.com/avatars/123456789012345678/avatar.png)  
💀 **Banner:** [Click Here](https://cdn.discordapp.com/banners/123456789012345678/banner.png)  
💀 **Nitro Status:** ✅ Active  
💀 **Account Created On:** 🗓️ 2015-06-24  
💀 **IP Address (Leaked Data):** 🌍 102.91.4.82 (Nigeria)  
💀 **Last Activity:** 👀 10 mins ago  

███████████████████████████████████████████████████
█  🛠️  Process Completed! Stay Anonymous! ☠️  █
███████████████████████████████████████████████████

```

---

## ⚠️ Disclaimer
> **This 🛠️ is for 📚 educational & 🕵️‍♂️ research purposes only.** Ensure you have the necessary ✅ permissions and comply with the **📜 terms of service** of all platforms before using this 🛠️. The authors are **not responsible** for any misuse ❌ or damage ⚠️ caused.

---

## 📜 License
This project is **📖 open-source** and available under the 🏛️ MIT License.

---

## 🤝 Contributions
Feel free to contribute! Open a **📤 pull request** or report a 🐞 issue if you find any bugs.

---

## 📞 Contact
For any inquiries, reach out via **🐙 GitHub issues**.

---

🚀 **🎯 Happy OSINT Hunting!**
