# Task 2 – File Organizer & Duplicate Finder

## 📘 Overview
This task delivers a **simple and practical file management tool** that can:
1) Organize files into folders by **extension** or by **modified date**; and  
2) Detect **duplicate files** using content hash (SHA-256), with a safe mode (dry-run) by default.

The goal is to provide a minimal but useful utility that demonstrates clean structure, safe defaults, and extendable design. This is a **preliminary submission** and will be expanded in later milestones.

---

## ✨ Features (Preliminary)
- **Organize by extension**: e.g., `jpg/`, `pdf/`, `txt/`, `no_ext/`
- **Organize by date**: e.g., `2025/11/` based on file modified time
- **Recursive scan** under a source directory
- **Duplicate detection** via SHA-256 hashing
- **Dry-run by default** (prints plan, does not move files)
- **Apply mode** with `--apply` to actually move files
- Clear **summary report** at the end

---

## 🗂️ Structure
