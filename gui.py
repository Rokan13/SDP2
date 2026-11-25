import tkinter as tk
from tkinter import ttk, messagebox

from database import load_default_cases
from user_management import register_user, login_user
from user_progress import get_user_cases, get_user_dashboard, filter_user_cases
from case_management import get_case_details
from solve_case import submit_case_answer

REVEAL_SOLUTION_ON_WRONG = True
BG, DARK, ACCENT = "#f4f1ea", "#2b2d42", "#8d0801"
FONT, FONT_BOLD = ("Segoe UI", 11), ("Segoe UI", 11, "bold")
FONT_TITLE, FONT_HEAD = ("Segoe UI", 22, "bold"), ("Segoe UI", 16, "bold")


def make_text(parent, height=10):
    box = ttk.Frame(parent)
    text = tk.Text(box, wrap="word", font=FONT, state="disabled", relief="flat",
                   bg="white", padx=14, pady=10, height=height)
    scroll = ttk.Scrollbar(box, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    for tag, cfg in [
        ("section", {"font": ("Segoe UI", 13, "bold"), "foreground": "white", "background": DARK}),
        ("title", {"font": ("Segoe UI", 13, "bold"), "foreground": DARK}),
        ("label", {"font": FONT_BOLD, "foreground": ACCENT}),
        ("good", {"font": FONT_BOLD, "foreground": "#1b7f3b"}),
        ("bad", {"font": FONT_BOLD, "foreground": "#b00020"}),
    ]:
        text.tag_configure(tag, **cfg)
    text.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return box, text


def write(text, parts):
    text.configure(state="normal")
    text.delete("1.0", "end")
    for content, tag in parts:
        text.insert("end", content, tag) if tag else text.insert("end", content)
    text.configure(state="disabled")


val = lambda v: "-" if v in (None, "") else str(v)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CaseClosed")
        self.geometry("960x680")
        self.minsize(820, 600)
        self.configure(bg=BG)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, font=FONT)
        style.configure("TButton", font=FONT, padding=8)
        style.configure("Accent.TButton", font=FONT_BOLD, padding=10, background=ACCENT, foreground="white")
        style.map("Accent.TButton", background=[("active", "#a30b02")])
        style.configure("TRadiobutton", background="white", font=FONT)
        style.configure("Treeview", font=FONT, rowheight=30)
        style.configure("Treeview.Heading", font=FONT_BOLD)

        self.user = None
        self.screen = ttk.Frame(self)
        self.screen.pack(fill="both", expand=True)
        self.show_welcome()

    def clear(self):
        for w in self.screen.winfo_children():
            w.destroy()

    def centered_card(self):
        self.clear()
        card = ttk.Frame(self.screen)
        card.place(relx=0.5, rely=0.5, anchor="center")
        return card

    # 1. Welcome
    def show_welcome(self):
        self.user = None
        card = self.centered_card()
        ttk.Label(card, text="CaseClosed", font=FONT_TITLE, foreground=ACCENT).pack(pady=(0, 4))
        ttk.Label(card, text="Welcome, detective.", font=("Segoe UI", 13)).pack(pady=(0, 30))
        ttk.Button(card, text="Registration", width=24, command=self.show_register).pack(pady=8)
        ttk.Button(card, text="Login", width=24, command=self.show_login).pack(pady=8)

    # 2. Registration
    def show_register(self):
        card = self.centered_card()
        ttk.Label(card, text="Registration", font=FONT_HEAD).grid(row=0, columnspan=2, pady=(0, 20))
        vars_ = [tk.StringVar() for _ in range(4)]

        def submit(e=None):
            u, em, pw, cpw = vars_[0].get().strip(), vars_[1].get().strip(), vars_[2].get(), vars_[3].get()
            if not all([u, em, pw, cpw]):
                return messagebox.showwarning("Registration", "Please fill in all fields.")
            if "@" not in em or "." not in em.split("@")[-1]:
                return messagebox.showwarning("Registration", "Please enter a valid email.")
            if pw != cpw:
                return messagebox.showwarning("Registration", "Passwords do not match.")
            try:
                if register_user(u, em, pw):
                    messagebox.showinfo("Registration", "Account created! Please log in.")
                    self.show_login()
                else:
                    messagebox.showerror("Registration", "Username or email already exists.")
            except ValueError as err:
                messagebox.showwarning("Registration", str(err))

        for i, (lbl, var, mask) in enumerate(zip(["User Name:", "Email:", "New Pass:", "Confirm Pass:"], vars_, ["", "", "*", "*"]), 1):
            ttk.Label(card, text=lbl).grid(row=i, column=0, sticky="e", padx=8, pady=6)
            ent = ttk.Entry(card, textvariable=var, show=mask, width=30, font=FONT)
            ent.grid(row=i, column=1, pady=6)
            ent.bind("<Return>", submit)

        btns = ttk.Frame(card)
        btns.grid(row=5, columnspan=2, pady=(20, 0))
        ttk.Button(btns, text="Submit", style="Accent.TButton", command=submit).pack(side="left", padx=6)
        ttk.Button(btns, text="Login", command=self.show_login).pack(side="left", padx=6)
        ttk.Button(btns, text="Back", command=self.show_welcome).pack(side="left", padx=6)

    # 3. Login
    def show_login(self):
        card = self.centered_card()
        ttk.Label(card, text="Login", font=FONT_HEAD).grid(row=0, columnspan=2, pady=(0, 20))
        u_var, p_var = tk.StringVar(), tk.StringVar()

        def login(e=None):
            u, p = u_var.get().strip(), p_var.get()
            if not u or not p:
                return messagebox.showwarning("Login", "Enter username and password.")
            user = login_user(u, p)
            if not user:
                return messagebox.showerror("Login", "Invalid username or password.")
            self.user = user
            self.show_dashboard()

        ttk.Label(card, text="User Name:").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        u_ent = ttk.Entry(card, textvariable=u_var, width=30, font=FONT)
        u_ent.grid(row=1, column=1, pady=6)
        ttk.Label(card, text="Pass:").grid(row=2, column=0, sticky="e", padx=8, pady=6)
        p_ent = ttk.Entry(card, textvariable=p_var, show="*", width=30, font=FONT)
        p_ent.grid(row=2, column=1, pady=6)
        p_ent.bind("<Return>", login)

        btns = ttk.Frame(card)
        btns.grid(row=3, columnspan=2, pady=(20, 0))
        ttk.Button(btns, text="Login", style="Accent.TButton", command=login).pack(side="left", padx=6)
        ttk.Button(btns, text="Back", command=self.show_welcome).pack(side="left", padx=6)
        u_ent.focus()

    # 4. User Dashboard
    def show_dashboard(self):
        card = self.centered_card()
        ttk.Label(card, text=f"Welcome, {self.user['username']}", font=FONT_TITLE, foreground=ACCENT).pack(pady=(0, 6))
        s = get_user_dashboard(self.user["user_id"])
        ttk.Label(card, text=f"Total: {s['total_cases']}    Solved: {s['solved_cases']}    Unsolved: {s['unsolved_cases']}",
                  font=("Segoe UI", 12)).pack(pady=(0, 28))

        for label, mode in [("View all cases", "all"), ("Solved case", "Solved"), ("Unsolved case", "Unsolved")]:
            ttk.Button(card, text=label, width=28, command=lambda m=mode: self.show_cases(m)).pack(pady=7)
        ttk.Button(card, text="Log out", width=28, command=self.show_welcome).pack(pady=(22, 0))

    # 5. View all cases
    def show_cases(self, mode="all"):
        self.clear()
        titles = {"all": "All Cases", "Solved": "Solved Cases", "Unsolved": "Unsolved Cases"}

        top = ttk.Frame(self.screen)
        top.pack(fill="x", padx=20, pady=(16, 6))
        ttk.Button(top, text="< Dashboard", command=self.show_dashboard).pack(side="left")
        ttk.Label(top, text=titles[mode], font=FONT_HEAD).pack(side="left", padx=20)

        filters = ttk.Frame(self.screen)
        filters.pack(fill="x", padx=20, pady=6)
        t_var, d_var, s_var = tk.StringVar(value="All"), tk.StringVar(value="All"), tk.StringVar(value="All")
        types = ["All"] + sorted({c["case_type"] for c in filter_user_cases(self.user["user_id"])})

        for lbl, var, vals, w in [("Type:", t_var, types, 16), ("Difficulty:", d_var, ["All", "Easy", "Medium", "Hard"], 10)]:
            ttk.Label(filters, text=lbl).pack(side="left")
            ttk.Combobox(filters, textvariable=var, state="readonly", width=w, values=vals).pack(side="left", padx=(4, 14))
        if mode == "all":
            ttk.Label(filters, text="Status:").pack(side="left")
            ttk.Combobox(filters, textvariable=s_var, state="readonly", width=10,
                         values=["All", "Solved", "Unsolved"]).pack(side="left", padx=(4, 14))

        tree = ttk.Treeview(self.screen, columns=("id", "title", "type", "diff", "status"), show="headings", selectmode="browse")
        for k, (lbl, w) in [("id", ("Case ID", 80)), ("title", ("Case Title", 320)), ("type", ("Type", 150)),
                            ("diff", ("Difficulty", 100)), ("status", ("Status", 100))]:
            tree.heading(k, text=lbl)
            tree.column(k, width=w, anchor="w")
        tree.tag_configure("Solved", foreground="#1b7f3b")
        tree.tag_configure("Unsolved", foreground="#b00020")
        tree.pack(fill="both", expand=True, padx=20, pady=8)

        def load():
            try:
                cases = filter_user_cases(
                    self.user["user_id"],
                    case_type=None if t_var.get() == "All" else t_var.get(),
                    status=(None if s_var.get() == "All" else s_var.get()) if mode == "all" else mode,
                    difficulty_level=None if d_var.get() == "All" else d_var.get()
                )
            except ValueError as err:
                return messagebox.showerror("Cases", str(err))
            tree.delete(*tree.get_children())
            for c in cases:
                tree.insert("", "end", iid=c["case_id"],
                            values=(c["case_id"], c["case_title"], c["case_type"], c["difficulty_level"], c["status"]),
                            tags=(c["status"],))

        def open_case(e=None):
            sel = tree.selection()
            if not sel:
                return messagebox.showinfo("Cases", "Please select a case first.")
            self.show_case_detail(sel[0], mode)

        ttk.Button(filters, text="Apply", command=load).pack(side="left")
        tree.bind("<Double-1>", open_case)

        bottom = ttk.Frame(self.screen)
        bottom.pack(fill="x", padx=20, pady=(0, 16))
        ttk.Label(bottom, text="Double-click a case or select it and press Open.").pack(side="left")
        ttk.Button(bottom, text="Open Case", style="Accent.TButton", command=open_case).pack(side="right")
        load()

    # 6. Case details -> Choose suspect -> Solution
    def show_case_detail(self, case_id, mode="all"):
        self.clear()
        try:
            details = get_case_details(case_id)
        except ValueError as err:
            messagebox.showerror("Case", str(err))
            return self.show_cases(mode)

        c, suspects = details["case"], details["suspects"]
        top = ttk.Frame(self.screen)
        top.pack(fill="x", padx=20, pady=(16, 6))
        ttk.Button(top, text="< Back to cases", command=lambda: self.show_cases(mode)).pack(side="left")
        ttk.Label(top, text=c["case_title"], font=FONT_HEAD).pack(side="left", padx=20)

        bottom = ttk.Frame(self.screen)
        bottom.pack(side="bottom", fill="x", padx=20, pady=(6, 16))
        sol_box, sol_text = make_text(bottom, height=7)
        box, main_text = make_text(self.screen)
        box.pack(fill="both", expand=True, padx=20, pady=6)

        def fill_page():
            status = next((r["status"] for r in get_user_cases(self.user["user_id"]) if r["case_id"] == case_id), "Unsolved")
            parts = [
                (" CASE INFO \n\n", "section"),
                ("Title: ", "label"), (f"{c['case_title']}\n", None), ("Type: ", "label"), (f"{c['case_type']}\n", None),
                ("Description: ", "label"), (f"{c['description']}\n", None), ("Location: ", "label"), (f"{val(c.get('location'))}\n", None),
                ("Date: ", "label"), (f"{val(c.get('incident_date'))}\n", None), ("Status: ", "label"), (f"{status}\n\n", None),
                (f" SUSPECTS ({len(suspects)}) \n\n", "section"),
            ]
            if not suspects:
                parts.append(("No suspects added.\n", None))
            for s in suspects:
                parts += [(f"{s['name']}\n", "title"), ("Age: ", "label"), (f"{val(s.get('age'))}\n", None),
                          ("Occupation: ", "label"), (f"{val(s.get('occupation'))}\n", None), ("Address: ", "label"), (f"{val(s.get('address'))}\n\n", None)]
            parts.append((" STATEMENTS \n\n", "section"))
            if not details["statements"]:
                parts.append(("No statements recorded.\n\n", None))
            for st in details["statements"]:
                parts += [(f"{st['suspect_name']}\n", "title"), ("Statement: ", "label"), (f"{st['statement']}\n", None),
                          ("Alibi: ", "label"), (f"{val(st.get('alibi'))}\n\n", None)]
            parts.append((" EVIDENCE \n\n", "section"))
            if not details["evidence"]:
                parts.append(("No evidence recorded.\n", None))
            for i, ev in enumerate(details["evidence"], 1):
                parts += [(f"{i}. ", "label"), (f"{val(ev.get('description'))}\n\n", None)]
            write(main_text, parts)

        def open_choose_dialog():
            if not suspects:
                return messagebox.showinfo("Choose suspect", "This case has no suspects.")
            dlg = tk.Toplevel(self)
            dlg.title("Choose suspect")
            dlg.configure(bg="white", padx=24, pady=18)
            dlg.transient(self)
            dlg.resizable(False, False)
            ttk.Label(dlg, text="Who is the culprit?", font=FONT_HEAD, background="white").pack(anchor="w", pady=(0, 10))
            choice = tk.IntVar(value=0)
            for s in suspects:
                ttk.Radiobutton(dlg, text=s["name"], value=s["suspect_id"], variable=choice).pack(anchor="w", pady=4)

            def confirm():
                if choice.get() <= 0:
                    return messagebox.showinfo("Choose suspect", "Please select a suspect.", parent=dlg)
                try:
                    res = submit_case_answer(self.user["user_id"], case_id, choice.get())
                except ValueError as err:
                    return messagebox.showerror("Choose suspect", str(err), parent=dlg)
                dlg.destroy()
                parts = [("Correct! You solved the case.\n\n", "good")] if res["is_correct"] else [("Wrong suspect.\n\n", "bad")]
                if res["is_correct"] or REVEAL_SOLUTION_ON_WRONG:
                    parts += [("Real culprit: ", "label"), (f"{res['culprit_name']}\n", None),
                              ("Description: ", "label"), (f"{res['explanation']}\n", None)]
                else:
                    parts.append(("Try again with another suspect.", None))
                sol_box.pack(fill="x", pady=(10, 0))
                write(sol_text, parts)
                fill_page()

            btns = ttk.Frame(dlg)
            btns.pack(anchor="e", pady=(14, 0))
            ttk.Button(btns, text="Submit", style="Accent.TButton", command=confirm).pack(side="left", padx=4)
            ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side="left", padx=4)
            dlg.grab_set()

        ttk.Button(bottom, text="Choose suspect", style="Accent.TButton", command=open_choose_dialog).pack(anchor="w")
        fill_page()


if __name__ == "__main__":
    load_default_cases()
    App().mainloop()