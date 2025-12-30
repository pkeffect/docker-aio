# Docker Container Manager (AIO)

A lightweight, cross-platform Python CLI tool designed to simplify Docker container management. 

While Docker is powerful, remembering container names and typing verbose commands (`docker exec -it <id> /bin/bash`, `docker logs -f <id>`) can be slow. This tool provides an interactive menu to instantly shell into containers, stop services, and—most importantly—**rapidly set up a multi-container monitoring environment.**

## 🚀 Key Features

*   **⚡ Instant Access:** No more copy-pasting Container IDs. Select containers by simple numbers.
*   **📝 Live Log Streaming:** One-key access to tail logs (`-f`) for any running container.
*   **💻 Smart Shell Detection:** Automatically attempts to connect via `/bin/bash`, `/bin/ash` (Alpine), and `/bin/sh` in that order.
*   **🛑 Quick Stop:** Gracefully stop containers without memorizing IDs.
*   **🎨 Cross-Platform:** Works seamlessly on Windows (cmd/powershell), macOS, and Linux with color-coded output.

## 👁️ Usage: Monitoring Multiple Containers Simultaneously

The primary strength of this tool is the ability to create a "dashboard" of logs on your screen in seconds without complex third-party UI tools.

**The Workflow:**
If you need to debug an interaction between three services (e.g., `web-app`, `api-server`, and `db`), the standard CLI method requires three long commands in three windows.

**With Docker AIO:**
1. Open **Terminal 1** -> Run script -> Press `1` -> Press `L`. (Streaming `web-app`)
2. Open **Terminal 2** -> Run script -> Press `2` -> Press `L`. (Streaming `api-server`)
3. Open **Terminal 3** -> Run script -> Press `3` -> Press `L`. (Streaming `db`)

Because the menu lists running containers dynamically, you can spin up a "Split View" monitoring station in under 5 seconds.

## 📋 Prerequisites

*   **Python 3.6+**
*   **Docker:** Docker must be installed and the daemon must be running.
*   **Permissions:** The user running the script must have permission to execute docker commands (e.g., be in the `docker` group on Linux).

## 🛠️ Installation

1. **Download the script**
   Save the file as `docker_aio.py`.

2. **Install Dependencies**
   The script relies on `colorama` for cross-platform coloring.
   ```bash
   pip install colorama
   ```

## 🎮 How to Run

Open your terminal and run:

```bash
python docker_aio.py
```

### Main Menu
The script scans for running containers immediately.
```text
  [1] my-web-server
  [2] redis-cache
  [3] worker-node

Options:
  [#] Enter number to select container
  [R] Refresh list
  [Q] Quit
```

### Action Menu
Once a container is selected, you have the following controls:
*   **[S] Shell:** Drops you immediately into the container's terminal.
*   **[L] Logs:** Streams live logs (Standard Output/Error). Press `Ctrl+C` to return to the menu (does not kill the container).
*   **[D] Stop:** Sends a stop signal to the container and returns you to the main list.
*   **[B] Back:** Return to container selection.

## 🔧 Troubleshooting

**"Error: 'docker' command not found"**
*   Ensure Docker is installed and added to your system's PATH variable.

**"Error: Docker daemon is not running..."**
*   **Windows/Mac:** Ensure Docker Desktop is open.
*   **Linux:** Ensure the service is active (`sudo systemctl start docker`).

**"Permission Denied"**
*   On Linux, if you need `sudo` to run docker commands, you will need to run this script with `sudo`:
    ```bash
    sudo python docker_aio.py
    ```
    *(Note: It is recommended to add your user to the `docker` group instead).*

## 📜 License

Free and open-source. Feel free to modify for your personal workflow.