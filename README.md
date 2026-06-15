<div align="center">

# 🔄 MorphX
### Multi-Format File Converter for Windows

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Release](https://img.shields.io/badge/release-stable-brightgreen.svg)

**Convert PDF · DOCX · PPTX · JPG · PNG · JPEG — fully offline, fully private.**

[⬇️ Download Installer](https://github.com/atif929/MorphX-File-Converter/releases/latest) · [🐛 Report Bug](https://github.com/atif929/MorphX-File-Converter/issues) · [💡 Request Feature](https://github.com/atif929/MorphX-File-Converter/issues)

![MorphX Screenshot](assets/screenshot.png)

</div>

---

## 📌 Purpose

MorphX is a lightweight, offline-first desktop utility built for Windows that enables seamless conversion between the most commonly used document and image formats. Whether you need to convert a PDF into an editable Word document, transform a PowerPoint presentation into images, or simply switch between image formats — MorphX handles it all in a single click, with zero internet dependency and zero data collection.

---

## ✨ Features

- 🔄 **Full Bidirectional Conversion** — every supported format converts to every other
- 🔒 **100% Offline** — no internet, no cloud, no data leaves your machine
- 🖥️ **Native Windows App** — built with PyQt6, feels like a real desktop app
- 📁 **Drag & Drop Support** — drop files directly into the app
- 📦 **Batch Conversion** — convert multiple files at once
- 📊 **Live Progress Tracking** — real-time progress bar and conversion log
- 🎨 **Modern UI** — clean light theme with blue accent design
- ⚡ **No Python Required** — fully packaged `.exe` installer

---

## 🔄 Supported Conversions

| From ↓ / To → | PDF | DOCX | PPTX | JPG | PNG | JPEG |
|---|---|---|---|---|---|---|
| **PDF** | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| **DOCX** | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| **PPTX** | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| **JPG** | ✅ | ✅ | ✅ | — | ✅ | ✅ |
| **PNG** | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| **JPEG** | ✅ | ✅ | ✅ | ✅ | ✅ | — |

---

## 📦 Installation

### Option 1 — Windows Installer (Recommended)

1. Go to [Releases](https://github.com/atif929/MorphX-File-Converter/releases/latest)
2. Download `MorphX_Setup_v1.0.0.exe`
3. Double-click to run the installer
4. Follow the setup wizard — click **Next** → **Install**
5. MorphX will appear in:
   - 🖥️ **Desktop** shortcut
   - 📌 **Start Menu** under MorphX
6. Double-click the shortcut to launch

> ✅ No Python. No pip. No terminal. Just install and run.

---

### Option 2 — Run from Source (Developers)

**Prerequisites:**
- Python 3.12
- Microsoft Word & PowerPoint (for DOCX/PPTX conversions)
- [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)

**Steps:**

```bash
# 1. Clone the repository
git clone https://github.com/atif929/MorphX-File-Converter.git
cd MorphX-File-Converter

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Poppler path in app/config.py
POPPLER_PATH = r"C:\path\to\poppler\bin"

# 5. Run the app
python main.py
```

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| UI Framework | PyQt6 |
| PDF Processing | pdf2image, pdf2docx |
| Office Conversion | Microsoft Office COM (comtypes, pywin32) |
| Image Processing | Pillow |
| Presentation | python-pptx |
| Word Documents | python-docx |
| Packaging | PyInstaller |
| Installer | Inno Setup 6 |

---

## 🔧 Building from Source

### Step 1 — Install Poppler

Download [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) and copy the bin folder:

```bash
xcopy /E /I "C:\poppler\Library\bin" "poppler_bin"
```

Update `POPPLER_PATH` in `app/config.py` accordingly.

### Step 2 — Build the Executable

```bash
venv\Scripts\python.exe -m PyInstaller converter.spec --clean --noconfirm
```

Output: `dist\MorphX\MorphX.exe`

### Step 3 — Create Windows Installer (Inno Setup)

1. Download and install [Inno Setup 6](https://jrsoftware.org/download.php/is.exe)
2. Open `installer.iss` in Inno Setup
3. Press `F9` to compile
4. Output: `installer_output\MorphX_Setup_v1.0.0.exe`

---

## 📋 System Requirements

| Requirement | Details |
|---|---|
| OS | Windows 10 / Windows 11 (64-bit) |
| Disk Space | ~120 MB |
| Python | ❌ Not required (for installer) |
| Internet | ❌ Not required |
| Microsoft Word | ✅ Recommended for DOCX conversions |
| Microsoft PowerPoint | ✅ Recommended for PPTX conversions |

---

## ⚠️ Known Limitations

- DOCX and PPTX conversions work best with **Microsoft Office installed**
- On systems without Microsoft Office, a fallback engine (`pdf2docx`) is used which may produce slightly reduced formatting fidelity
- PDF → PPTX conversion embeds pages as images (not editable text slides)

---

## 🗑️ Uninstalling

- **Settings** → **Apps** → search **MorphX** → **Uninstall**
- Or **Control Panel** → **Programs and Features** → **MorphX** → **Uninstall**

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Atif Rameez**
- GitHub: [@atif929](https://github.com/atif929)
- LinkedIn: [Atif on LinkedIn](https://www.linkedin.com/in/atif-rameez-b92ba7390/)

---

<div align="center">

*Built with ❤️  by Atif Rameez— open source, free forever.*

⭐ Star this repo if MorphX helped you!

</div>