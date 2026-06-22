<div align="center">

#  Expense Tracker

### A sleek, dark-themed desktop expense tracker built with Python & Tkinter

![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Dependencies](https://img.shields.io/badge/Dependencies-Zero-success?style=flat-square)

No external dependencies. No database setup. Just clone and run.

</div>

---


##  Features

- ➕ **Add expenses** — description, amount, category & date
- 🗑️ **Delete entries** — one-click removal with confirmation
- 🔍 **Filter by category** — Food, Transport, Bills, Shopping, and more
- 📊 **Live monthly summary** — total spend + category-wise breakdown
- 📤 **Export to CSV** — generate timestamped backups anytime
- 💾 **Persistent storage** — all data saved locally in `expenses.csv`
- 🎨 **Modern dark UI** — built entirely with native Tkinter widgets

---

##  Tech Stack

This project intentionally uses **zero third-party packages** — everything is pure Python standard library.

| Module | Purpose |
|---|---|
| `tkinter` | GUI framework (windows, widgets, styling) |
| `csv` | Reading/writing expense records |
| `os` | Checking if the data file exists |
| `datetime` | Date validation & monthly filtering |

---

##  Getting Started

### Prerequisites
- Python 3.7 or higher
- Tkinter (comes pre-installed with Python on Windows/macOS; on Linux install via `sudo apt-get install python3-tk` if missing)

### Installation

```bash
# Clone the repository
git clone https://github.com/0ByteBuilder1/expense-tracker.git
cd expense-tracker

# Run the app — no pip install required!
python expense_tracker.py
```

That's it. The app will auto-create `expenses.csv` on first launch.

---

##  Project Structure

```
expense-tracker/
│
├── expense_tracker.py   # Main application (GUI + logic)
├── expenses.csv         # Auto-generated data file (created on first run)
└── README.md            # You are here
```

---

##  How It Works

1. On launch, the app checks if `expenses.csv` exists — if not, it creates one with headers.
2. Every **Add Expense** call appends a new row with an auto-incremented ID.
3. The **Treeview table** reloads from the CSV on every change, so the UI always reflects the file on disk.
4. The **summary panel** recalculates monthly totals and per-category spend live.
5. **Export** simply copies the current CSV with a timestamped filename — instant backup.

---

##  Roadmap / Future Improvements

- [ ] Add expense charts using `matplotlib`
- [ ] Set monthly budget limits with overspend alerts
- [ ] Switch storage to SQLite for larger datasets
- [ ] Add multi-user login support
- [ ] Dark/light theme toggle

---

##  Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

##  License

This project is licensed under the **MIT License** — feel free to use it for learning, academic submissions, or personal projects.

---

<div align="center">

Made with Python and coffee

</div>
