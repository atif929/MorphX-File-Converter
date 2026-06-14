# ⚡ MorphX File Converter

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/UI%20Framework-PyQt6-007aff)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

MorphX is a premium, open-source cross-platform desktop application engineered for high-performance multi-format file conversion. Featuring a refined light-theme interface inspired by Apple design primitives, MorphX blends advanced glassmorphism visuals, smooth interactive hover neon glow mechanics, and multi-threaded asynchronous processing into a clean layout.

---

## 🎯 Project Goal

The primary goal of MorphX is to remove the dependency on clunky, ad-heavy web-based file converters. It provides a secure, completely offline alternative where users can queue, filter, and convert multiple media and document types seamlessly on their local machine.

### ✨ Key Features

* ☁️ **Interactive Drop Zone:** Click or drag-and-drop file queues with automated extension verification.
* 💎 **Glassmorphic Light Theme:** Crisp, modern palette (`#f0f4ff` canvas) combined with premium Apple-inspired light components.
* 💡 **Hyper-Glow Interactive UI:** Buttons and border lines that ignite custom neon colors and glass alpha levels on hover.
* 🧵 **Asynchronous Workloads:** High-speed background conversion threads that prevent the UI loop from locking up.
* 🔒 **Local & Secure:** No cloud transfers. Files are managed entirely within your local execution loop.

---

## 🛠️ The Tech Stack

* **Language:** Python 3.10+
* **UI Framework:** `PyQt6` (Core window rendering, layout engines, and signal/slot event pipelines)
* **Styling System:** Advanced Qt Style Sheets (`QSS`) utilizing linear color gradients and relative positioning.
* **OS Engine:** `ctypes` (Win32 process unlinking wrapper for native taskbar icon management)

---

## 🚀 Getting Started (Local Installation)

Follow these simple steps to clone, configure, and boot the desktop layout environment locally on your machine.

### Prerequisites

* Ensure you have [Python 3.10 or higher](https://www.python.org/downloads/) installed.
* Make sure `git` is configured on your local workstation.

### Step 1: Clone the Repository

```bash
git clone [https://github.com/atif929/MorphX-File-Converter.git](https://github.com/atif929/MorphX-File-Converter.git)
cd MorphX-File-Converter
