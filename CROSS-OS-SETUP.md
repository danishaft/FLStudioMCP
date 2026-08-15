# Cross-OS Setup Guide

## Disk Layout (Target)

```
nvme0n1 (476.9GB)
├── p1: EFI (1GB)          — boot/efi, shared
├── p2: Linux ext4 (~200GB) — Ubuntu, shrunk
├── p3: Windows NTFS (~150GB) — Windows 11
└── p4: Shared NTFS (~125GB) — cross-OS project data
```

## Step 1: Shrink Linux + Create Shared Partition

Run from Linux BEFORE installing Windows:

```bash
# Install ntfs-3g for NTFS support
sudo apt install ntfs-3g gparted -y

# Shrink Linux partition (from ~475GB to ~200GB)
# GParted is safer for this — boot from live USB or run from Linux
sudo gparted /dev/nvme0n1
```

In GParted:
1. Right-click nvme0n1p2 (ext4) → Resize → 200GB
2. In the freed space, create:
   - p3: NTFS, 150GB, label "WINDOWS"
   - p4: NTFS, 125GB, label "SHARED"

## Step 2: Copy Project to Shared Partition

```bash
# Format shared partition
sudo mkntfs -f -L SHARED /dev/nvme0n1p4

# Mount it
sudo mkdir -p /mnt/shared
sudo mount /dev/nvme0n1p4 /mnt/shared

# Copy project data
sudo mkdir -p /mnt/shared/home/ayodele/Desktop
sudo cp -r ~/Desktop/flmcp /mnt/shared/home/ayodele/Desktop/

sudo mkdir -p /mnt/shared/home/ayodele/.codex/agents
sudo cp -r ~/.codex/agents/* /mnt/shared/home/ayodele/.codex/agents/

sudo mkdir -p /mnt/shared/home/ayodele/.config/opencode
sudo cp -r ~/.config/opencode/* /mnt/shared/home/ayodele/.config/opencode/

sudo mkdir -p /mnt/shared/home/ayodele/.agents/skills
sudo cp -r ~/.agents/skills/* /mnt/shared/home/ayodele/.agents/skills/

sudo umount /mnt/shared
```

## Step 3: Install Windows from Ventoy USB

1. Download Windows 11 ISO from https://www.microsoft.com/software-download/windows11
2. Copy ISO to Ventoy USB
3. Reboot → enter BIOS (F2/F12) → boot from USB
4. Select Windows ISO in Ventoy menu
5. Install Windows on p3 (NTFS 150GB)
6. When prompted, DON'T touch p4 (SHARED) — leave it alone

## Step 4: After Windows is Installed

### On Windows:
1. Install OpenCode: https://opencode.ai
2. Copy shared data:
   ```
   # Open PowerShell as Admin
   # The SHARED partition will auto-mount (e.g. D:\ or E:\)
   xcopy "D:\home\ayodele\Desktop\flmcp" "%USERPROFILE%\Desktop\flmcp" /E /I
   xcopy "D:\home\ayodele\.codex" "%USERPROFILE%\.codex" /E /I
   xcopy "D:\home\ayodele\.config\opencode" "%USERPROFILE%\.config\opencode" /E /I
   ```
3. Install Python 3.13 from python.org
4. Install Go from https://go.dev/dl/
5. Rebuild CLI: `cd Desktop/flmcp && pip install -e . && clihub generate`
6. Verify: `flmcp transport-status -o json`

### On Linux (still works):
1. Mount shared: `sudo mount /dev/nvme0n1p4 /mnt/shared`
2. Access project: `cd /mnt/shared/home/ayodele/Desktop/flmcp`

## Step 5: Auto-Mount Shared on Linux

```bash
# Add to /etc/fstab:
echo '/dev/nvme0n1p4 /mnt/shared ntfs-3g defaults,uid=1000,gid=1000,rw 0 0' | sudo tee -a /etc/fstab
```

## What's Shared

| Path | Contains |
|---|---|
| `~/Desktop/flmcp/` | Full project (PRD, tests, bridge, CLI) |
| `~/.codex/agents/merlin.md` | Merlin agent definition |
| `~/.codex/agents/brain/` | Memory system |
| `~/.config/opencode/` | OpenCode config |
| `~/.agents/skills/` | Custom skills |

## Session Continuity

After setup:
1. On Linux: `opencode` reads from shared partition → same project
2. On Windows: `opencode` reads from same shared partition → same project
3. PRD, agents, tests, memory — all identical across both OSes
4. FL Studio runs natively on Windows → no more Wine issues
5. `flmcp` CLI works on both → same commands

