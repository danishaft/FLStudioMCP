#!/bin/bash
# migrate-to-shared.sh — Copy project data to shared NTFS partition
# Run from Linux BEFORE installing Windows

set -e

SHARED_LABEL="SHARED"
SHARED_DEV=""
MNT="/mnt/shared"
PROJECT_DIR="$HOME/Desktop/flmcp"

# Find SHARED partition
for dev in /dev/nvme0n1p4 /dev/sda1; do
    if blkid "$dev" 2>/dev/null | grep -q "$SHARED_LABEL"; then
        SHARED_DEV="$dev"
        break
    fi
done

if [ -z "$SHARED_DEV" ]; then
    echo "ERROR: No partition with label '$SHARED_LABEL' found."
    echo "Run GParted first to create the shared partition."
    echo ""
    echo "Steps:"
    echo "1. sudo gparted /dev/nvme0n1"
    echo "2. Shrink Linux (nvme0n1p2) to ~200GB"
    echo "3. Create NTFS partition in freed space, label it SHARED"
    echo "4. Run this script again"
    exit 1
fi

echo "=== Found shared partition: $SHARED_DEV ==="

# Create mount point
sudo mkdir -p "$MNT"

# Mount
echo "=== Mounting $SHARED_DEV ==="
sudo mount "$SHARED_DEV" "$MNT" || {
    echo "Mount failed. Formatting as NTFS..."
    sudo mkntfs -f -L "$SHARED_LABEL" "$SHARED_DEV"
    sudo mount "$SHARED_DEV" "$MNT"
}

echo "=== Copying project files ==="

# flmcp project
mkdir -p "$MNT/home/ayodele/Desktop"
cp -r "$PROJECT_DIR" "$MNT/home/ayodele/Desktop/"
echo "  Copied: flmcp/"

# Merlin agent + brain
mkdir -p "$MNT/home/ayodele/.codex/agents"
cp -r "$HOME/.codex/agents/"* "$MNT/home/ayodele/.codex/agents/" 2>/dev/null || true
echo "  Copied: .codex/agents/"

# OpenCode config
mkdir -p "$MNT/home/ayodele/.config/opencode"
cp -r "$HOME/.config/opencode/"* "$MNT/home/ayodele/.config/opencode/" 2>/dev/null || true
echo "  Copied: .config/opencode/"

# Skills
if [ -d "$HOME/.agents/skills" ]; then
    mkdir -p "$MNT/home/ayodele/.agents/skills"
    cp -r "$HOME/.agents/skills/"* "$MNT/home/ayodele/.agents/skills/" 2>/dev/null || true
    echo "  Copied: .agents/skills/"
fi

echo ""
echo "=== Done! Shared partition contents: ==="
find "$MNT" -maxdepth 4 -type d | head -30
echo ""
echo "=== Next steps: ==="
echo "1. Download Windows 11 ISO to Ventoy USB"
echo "2. Boot from USB"
echo "3. Install Windows on the other NTFS partition (NOT this SHARED one)"
echo "4. After Windows install, see CROSS-OS-SETUP.md Step 4"
