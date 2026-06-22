import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

# ──────────────────────────────────────────────
#  FILE SETUP
# ──────────────────────────────────────────────
FILE = "expenses.csv"
HEADERS = ["ID", "Date", "Category", "Description", "Amount"]
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"]

def init_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            csv.writer(f).writerow(HEADERS)

def read_expenses():
    with open(FILE, "r") as f:
        return list(csv.DictReader(f))

def write_expenses(expenses):
    with open(FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(expenses)

def next_id():
    expenses = read_expenses()
    return str(max((int(e["ID"]) for e in expenses), default=0) + 1)

# ──────────────────────────────────────────────
#  COLORS & FONTS
# ──────────────────────────────────────────────
BG       = "#1e1e2e"
SURFACE  = "#2a2a3e"
ACCENT   = "#7c3aed"
ACCENT2  = "#a855f7"
GREEN    = "#22c55e"
RED      = "#ef4444"
TEXT     = "#e2e8f0"
SUBTEXT  = "#94a3b8"
WHITE    = "#ffffff"

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_SMALL  = ("Segoe UI", 9)
FONT_BIG    = ("Segoe UI", 22, "bold")

# ──────────────────────────────────────────────
#  MAIN APP
# ──────────────────────────────────────────────
class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense Tracker")
        self.root.geometry("950x650")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        init_file()
        self.build_ui()
        self.refresh_table()
        self.update_summary()

    # ── LAYOUT ──────────────────────────────
    def build_ui(self):
        # Title bar
        title_bar = tk.Frame(self.root, bg=ACCENT, height=55)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="💰  Expense Tracker", font=FONT_TITLE,
                 bg=ACCENT, fg=WHITE).pack(side="left", padx=20, pady=10)
        tk.Label(title_bar, text="Track • Manage • Save", font=FONT_SMALL,
                 bg=ACCENT, fg="#ddd6fe").pack(side="right", padx=20)

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=15, pady=12)

        # Left: form + summary
        left = tk.Frame(body, bg=BG, width=280)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.pack_propagate(False)

        self.build_form(left)
        self.build_summary(left)

        # Right: table + filter
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)
        self.build_filter(right)
        self.build_table(right)
        self.build_action_buttons(right)

    # ── FORM ────────────────────────────────
    def build_form(self, parent):
        card = tk.Frame(parent, bg=SURFACE, padx=14, pady=14)
        card.pack(fill="x", pady=(0, 10))

        tk.Label(card, text="➕  Add Expense", font=FONT_BOLD,
                 bg=SURFACE, fg=ACCENT2).pack(anchor="w", pady=(0, 10))

        def field(label, widget_fn):
            tk.Label(card, text=label, font=FONT_SMALL, bg=SURFACE, fg=SUBTEXT).pack(anchor="w")
            w = widget_fn(card)
            w.pack(fill="x", pady=(2, 8))
            return w

        self.desc_var  = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.cat_var   = tk.StringVar(value=CATEGORIES[0])
        self.date_var  = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        def entry(p): return self._entry(p, self.desc_var)
        def amount_entry(p): return self._entry(p, self.amount_var)
        def cat_combo(p):
            cb = ttk.Combobox(p, textvariable=self.cat_var,
                              values=CATEGORIES, state="readonly", font=FONT_SMALL)
            self._style_combo(cb)
            return cb
        def date_entry(p): return self._entry(p, self.date_var)

        field("Description", entry)
        field("Amount (₹)", amount_entry)
        field("Category", cat_combo)
        field("Date (YYYY-MM-DD)", date_entry)

        btn = tk.Button(card, text="  Add Expense", font=FONT_BOLD,
                        bg=ACCENT, fg=WHITE, relief="flat", cursor="hand2",
                        activebackground=ACCENT2, activeforeground=WHITE,
                        command=self.add_expense, pady=8)
        btn.pack(fill="x", pady=(4, 0))

    def _entry(self, parent, var):
        e = tk.Entry(parent, textvariable=var, font=FONT_SMALL,
                     bg="#3b3b52", fg=TEXT, insertbackground=WHITE,
                     relief="flat", bd=6)
        return e

    def _style_combo(self, cb):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#3b3b52",
                        background="#3b3b52", foreground=TEXT,
                        arrowcolor=ACCENT2, borderwidth=0)
        style.map("TCombobox", fieldbackground=[("readonly", "#3b3b52")])

    # ── SUMMARY ─────────────────────────────
    def build_summary(self, parent):
        self.summary_card = tk.Frame(parent, bg=SURFACE, padx=14, pady=14)
        self.summary_card.pack(fill="x")

        tk.Label(self.summary_card, text="📊  This Month", font=FONT_BOLD,
                 bg=SURFACE, fg=ACCENT2).pack(anchor="w", pady=(0, 8))

        self.total_label = tk.Label(self.summary_card, text="₹0.00",
                                    font=FONT_BIG, bg=SURFACE, fg=GREEN)
        self.total_label.pack(anchor="w")

        tk.Label(self.summary_card, text="Total Spent", font=FONT_SMALL,
                 bg=SURFACE, fg=SUBTEXT).pack(anchor="w", pady=(0, 10))

        self.cat_frame = tk.Frame(self.summary_card, bg=SURFACE)
        self.cat_frame.pack(fill="x")

    def update_summary(self):
        for w in self.cat_frame.winfo_children():
            w.destroy()

        expenses = read_expenses()
        this_month = datetime.now().strftime("%Y-%m")
        monthly = [e for e in expenses if e["Date"].startswith(this_month)]
        total = sum(float(e["Amount"]) for e in monthly)

        self.total_label.config(text=f"₹{total:,.2f}")

        cat_totals = {}
        for e in monthly:
            cat_totals[e["Category"]] = cat_totals.get(e["Category"], 0) + float(e["Amount"])

        for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1])[:5]:
            row = tk.Frame(self.cat_frame, bg=SURFACE)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=cat, font=FONT_SMALL, bg=SURFACE, fg=TEXT).pack(side="left")
            tk.Label(row, text=f"₹{amt:,.0f}", font=FONT_SMALL, bg=SURFACE, fg=SUBTEXT).pack(side="right")

    # ── FILTER ──────────────────────────────
    def build_filter(self, parent):
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill="x", pady=(0, 8))

        tk.Label(bar, text="Filter:", font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(side="left")

        self.filter_var = tk.StringVar(value="All")
        cats = ["All"] + CATEGORIES
        for cat in cats:
            rb = tk.Radiobutton(bar, text=cat, variable=self.filter_var, value=cat,
                                font=FONT_SMALL, bg=BG, fg=SUBTEXT,
                                selectcolor=ACCENT, activebackground=BG,
                                activeforeground=ACCENT2, indicatoron=False,
                                relief="flat", padx=6, pady=3, cursor="hand2",
                                command=self.refresh_table)
            rb.pack(side="left", padx=1)

    # ── TABLE ───────────────────────────────
    def build_table(self, parent):
        cols = ("ID", "Date", "Category", "Description", "Amount")

        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=SURFACE, foreground=TEXT,
                        rowheight=30, fieldbackground=SURFACE,
                        font=FONT_SMALL, borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=ACCENT, foreground=WHITE,
                        font=FONT_BOLD, relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", WHITE)])

        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=cols, show="headings",
                                 style="Custom.Treeview", selectmode="browse")

        widths = {"ID": 45, "Date": 100, "Category": 110, "Description": 180, "Amount": 90}
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.column("Description", anchor="w")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        expenses = read_expenses()
        cat_filter = self.filter_var.get()

        for i, e in enumerate(expenses):
            if cat_filter != "All" and e["Category"] != cat_filter:
                continue
            tag = "even" if i % 2 == 0 else "odd"
            amount = f"₹{float(e['Amount']):,.2f}"
            self.tree.insert("", "end", iid=e["ID"],
                             values=(e["ID"], e["Date"], e["Category"],
                                     e["Description"], amount),
                             tags=(tag,))

        self.tree.tag_configure("even", background=SURFACE)
        self.tree.tag_configure("odd", background="#252538")

    # ── ACTION BUTTONS ───────────────────────
    def build_action_buttons(self, parent):
        bar = tk.Frame(parent, bg=BG)
        bar.pack(fill="x", pady=(8, 0))

        tk.Button(bar, text="🗑  Delete Selected", font=FONT_SMALL,
                  bg=RED, fg=WHITE, relief="flat", cursor="hand2",
                  activebackground="#b91c1c", activeforeground=WHITE,
                  command=self.delete_expense, padx=12, pady=6).pack(side="left", padx=(0, 8))

        tk.Button(bar, text="📤  Export CSV", font=FONT_SMALL,
                  bg="#0f766e", fg=WHITE, relief="flat", cursor="hand2",
                  activebackground="#0d9488", activeforeground=WHITE,
                  command=self.export_csv, padx=12, pady=6).pack(side="left")

        self.status_label = tk.Label(bar, text="", font=FONT_SMALL, bg=BG, fg=GREEN)
        self.status_label.pack(side="right", padx=8)

    # ── LOGIC ───────────────────────────────
    def add_expense(self):
        desc   = self.desc_var.get().strip()
        amount = self.amount_var.get().strip()
        cat    = self.cat_var.get()
        date   = self.date_var.get().strip()

        if not desc or not amount:
            messagebox.showwarning("Missing Info", "Please fill Description and Amount.")
            return
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Amount", "Enter a valid positive number.")
            return
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use format YYYY-MM-DD.")
            return

        expense = {"ID": next_id(), "Date": date, "Category": cat,
                   "Description": desc, "Amount": f"{amount:.2f}"}

        expenses = read_expenses()
        expenses.append(expense)
        write_expenses(expenses)

        self.desc_var.set("")
        self.amount_var.set("")
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))

        self.refresh_table()
        self.update_summary()
        self.set_status(f"✅ Added: {desc} — ₹{amount:.2f}")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing Selected", "Please select a row to delete.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected expense?"):
            return

        eid = selected[0]
        expenses = [e for e in read_expenses() if e["ID"] != eid]
        write_expenses(expenses)
        self.refresh_table()
        self.update_summary()
        self.set_status("🗑 Expense deleted.")

    def export_csv(self):
        import shutil
        export_name = f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        shutil.copy(FILE, export_name)
        self.set_status(f"📤 Exported to {export_name}")
        messagebox.showinfo("Exported", f"Saved as:\n{export_name}")

    def set_status(self, msg):
        self.status_label.config(text=msg)
        self.root.after(4000, lambda: self.status_label.config(text=""))


# ──────────────────────────────────────────────
#  RUN
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
