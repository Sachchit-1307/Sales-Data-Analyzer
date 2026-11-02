"""
=====================================================================
 SALES DATA ANALYZER
 A Tkinter desktop application built for a college mini-project.

 This project is designed to demonstrate the concepts taught in
 "Python Module 03: Python Data Structures":

     - Lists                  -> self.sales (list of dictionaries)
     - Tuples                 -> PRODUCT_CATALOG, table column headers
     - Sets                   -> unique products / categories / regions
     - Dictionaries           -> each sales record, aggregation results
     - List comprehensions    -> filtering / search / extracting fields
     - Dictionary comprehensions -> revenue-by-category, units-by-product
     - Set comprehensions     -> unique value extraction
     - String methods         -> lower(), upper(), split(), join()
     - Nested data structures -> list of dicts, dict of dicts/tuples
     - datetime module        -> date parsing, month grouping, validation

 Every screen in the sidebar is implemented as its own "page" that is
 rebuilt from the live `self.sales` list whenever it is opened, so the
 whole app always reflects the current data - add a sale and every
 analysis screen updates automatically.
=====================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import defaultdict

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------------------------------------------------------
# GLOBAL CONSTANTS
# ---------------------------------------------------------------------------

DATE_FORMAT = "%d-%m-%Y"

# A tuple is used here because the column layout of the Sales Records
# table is FIXED information that should never be modified at runtime.
TABLE_COLUMNS = ("Date", "Product", "Category", "Quantity", "Price", "Region", "Revenue")

# Dictionary of tuples: for each known product we store a fixed
# (category, suggested_price) pair. This lets the "Add Sale" form
# auto-fill the category and price when a known product is chosen -
# a meaningful, non-decorative use of dictionaries + tuples together.
PRODUCT_CATALOG = {
    "Laptop":      ("Electronics", 55000),
    "Smartphone":  ("Electronics", 25000),
    "Tablet":      ("Electronics", 18000),
    "Monitor":     ("Computers", 9000),
    "Keyboard":    ("Accessories", 800),
    "Mouse":       ("Accessories", 500),
    "Printer":     ("Computers", 7000),
    "Headphones":  ("Accessories", 1500),
}

REGIONS = ("Bangalore", "Mumbai", "Delhi", "Chennai", "Kolkata")

# ---------------------------------------------------------------------------
# COLOR THEME
# ---------------------------------------------------------------------------

COLOR_BG = "#0f172a"          # sidebar background (dark navy)
COLOR_BG_LIGHT = "#f1f5f9"    # main content background
COLOR_ACCENT = "#2563eb"      # accent blue
COLOR_ACCENT_DARK = "#1d4ed8"
COLOR_TEXT_LIGHT = "#e2e8f0"
COLOR_CARD = "#ffffff"
COLOR_SUCCESS = "#16a34a"
COLOR_DANGER = "#dc2626"
COLOR_MUTED = "#64748b"

FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_NAV = ("Segoe UI", 11)
FONT_CARD_VALUE = ("Segoe UI", 18, "bold")
FONT_CARD_LABEL = ("Segoe UI", 9)


# ---------------------------------------------------------------------------
# SAMPLE DATASET
# ---------------------------------------------------------------------------
# The core dataset is a LIST OF DICTIONARIES - one dictionary per sale.
# This is the central "nested data structure" used throughout the app.

def build_sample_dataset():
    raw = [
        ("02-01-2026", "Laptop", "Electronics", 3, 55000, "Bangalore"),
        ("04-01-2026", "Mouse", "Accessories", 10, 500, "Mumbai"),
        ("07-01-2026", "Smartphone", "Electronics", 5, 24000, "Delhi"),
        ("11-01-2026", "Keyboard", "Accessories", 8, 800, "Chennai"),
        ("15-01-2026", "Monitor", "Computers", 4, 9000, "Bangalore"),
        ("21-01-2026", "Printer", "Computers", 2, 7000, "Kolkata"),
        ("28-01-2026", "Headphones", "Accessories", 6, 1500, "Mumbai"),
        ("03-02-2026", "Laptop", "Electronics", 2, 56000, "Delhi"),
        ("09-02-2026", "Tablet", "Electronics", 4, 18000, "Chennai"),
        ("14-02-2026", "Smartphone", "Electronics", 7, 24500, "Bangalore"),
        ("18-02-2026", "Mouse", "Accessories", 12, 480, "Kolkata"),
        ("23-02-2026", "Monitor", "Computers", 3, 9200, "Mumbai"),
        ("02-03-2026", "Laptop", "Electronics", 4, 54500, "Chennai"),
        ("06-03-2026", "Keyboard", "Accessories", 9, 750, "Bangalore"),
        ("12-03-2026", "Printer", "Computers", 3, 7200, "Delhi"),
        ("19-03-2026", "Headphones", "Accessories", 5, 1600, "Kolkata"),
        ("25-03-2026", "Smartphone", "Electronics", 6, 24800, "Mumbai"),
        ("01-04-2026", "Tablet", "Electronics", 5, 17800, "Bangalore"),
        ("08-04-2026", "Monitor", "Computers", 6, 8900, "Chennai"),
        ("15-04-2026", "Laptop", "Electronics", 5, 55500, "Delhi"),
        ("22-04-2026", "Mouse", "Accessories", 15, 490, "Mumbai"),
        ("28-04-2026", "Keyboard", "Accessories", 7, 820, "Kolkata"),
        ("04-05-2026", "Smartphone", "Electronics", 8, 23900, "Bangalore"),
        ("11-05-2026", "Printer", "Computers", 4, 6900, "Chennai"),
        ("17-05-2026", "Headphones", "Accessories", 7, 1550, "Delhi"),
        ("24-05-2026", "Laptop", "Electronics", 3, 56200, "Mumbai"),
        ("02-06-2026", "Tablet", "Electronics", 6, 18200, "Kolkata"),
        ("09-06-2026", "Monitor", "Computers", 5, 9100, "Bangalore"),
        ("16-06-2026", "Smartphone", "Electronics", 9, 24200, "Chennai"),
        ("23-06-2026", "Mouse", "Accessories", 11, 510, "Delhi"),
        ("01-07-2026", "Laptop", "Electronics", 6, 55800, "Bangalore"),
        ("08-07-2026", "Keyboard", "Accessories", 10, 790, "Mumbai"),
        ("15-07-2026", "Printer", "Computers", 3, 7100, "Kolkata"),
        ("22-07-2026", "Headphones", "Accessories", 8, 1480, "Chennai"),
        ("29-07-2026", "Tablet", "Electronics", 4, 18100, "Delhi"),
        ("05-08-2026", "Smartphone", "Electronics", 10, 24700, "Bangalore"),
        ("12-08-2026", "Monitor", "Computers", 7, 9000, "Mumbai"),
        ("19-08-2026", "Laptop", "Electronics", 7, 56000, "Kolkata"),
        ("26-08-2026", "Mouse", "Accessories", 13, 495, "Chennai"),
        ("02-09-2026", "Keyboard", "Accessories", 12, 810, "Delhi"),
        ("09-09-2026", "Printer", "Computers", 5, 7050, "Bangalore"),
        ("15-09-2026", "Laptop", "Electronics", 2, 60000, "Bangalore"),
    ]
    sales = []
    for date_str, product, category, qty, price, region in raw:
        sales.append({
            "date": date_str,
            "product": product,
            "category": category,
            "quantity": qty,
            "price": price,
            "region": region,
        })
    return sales


# ---------------------------------------------------------------------------
# HELPER / ANALYSIS FUNCTIONS
# (kept outside the class so they clearly demonstrate the Module 03
#  data-structure concepts in isolation)
# ---------------------------------------------------------------------------

def calc_revenue(record):
    """Revenue = Quantity x Price."""
    return record["quantity"] * record["price"]


def format_currency(amount):
    return f"\u20b9{amount:,.2f}"


def safe_parse_date(date_str):
    """Parses a dd-mm-yyyy date string. Returns None on failure
    instead of crashing the application (graceful error handling)."""
    try:
        return datetime.strptime(date_str.strip(), DATE_FORMAT)
    except (ValueError, AttributeError):
        return None


def get_unique_products(sales):
    # SET COMPREHENSION - unique values only.
    return {s["product"] for s in sales}


def get_unique_categories(sales):
    return {s["category"] for s in sales}


def get_unique_regions(sales):
    return {s["region"] for s in sales}


def revenue_by_product(sales):
    # DICTIONARY COMPREHENSION built from a set of unique products.
    products = get_unique_products(sales)
    return {p: sum(calc_revenue(s) for s in sales if s["product"] == p) for p in products}


def units_by_product(sales):
    products = get_unique_products(sales)
    return {p: sum(s["quantity"] for s in sales if s["product"] == p) for p in products}


def revenue_by_category(sales):
    categories = get_unique_categories(sales)
    return {c: sum(calc_revenue(s) for s in sales if s["category"] == c) for c in categories}


def units_by_category(sales):
    categories = get_unique_categories(sales)
    return {c: sum(s["quantity"] for s in sales if s["category"] == c) for c in categories}


def revenue_by_region(sales):
    regions = get_unique_regions(sales)
    return {r: sum(calc_revenue(s) for s in sales if s["region"] == r) for r in regions}


def revenue_by_date(sales):
    dates = {s["date"] for s in sales}
    return {d: sum(calc_revenue(s) for s in sales if s["date"] == d) for d in dates}


def revenue_by_month(sales):
    """Groups revenue by 'Month Year' using the datetime module."""
    monthly = defaultdict(float)
    for s in sales:
        dt = safe_parse_date(s["date"])
        if dt:
            key = dt.strftime("%B %Y")
            monthly[key] += calc_revenue(s)
    return dict(monthly)


def top_n_products(sales, n=5):
    units = units_by_product(sales)
    # sorted() over a dictionary's items - list comprehension friendly result
    return sorted(units.items(), key=lambda item: item[1], reverse=True)[:n]


def low_performing_products(sales, threshold_ratio=0.5):
    """Products whose units sold are below `threshold_ratio` of the
    average units sold per product."""
    units = units_by_product(sales)
    if not units:
        return []
    average = sum(units.values()) / len(units)
    # LIST COMPREHENSION with a condition
    return [p for p, u in units.items() if u < average * threshold_ratio]


def generate_business_insights(sales):
    """Dynamically builds a list of insight strings purely from the
    current sales data - nothing here is hardcoded."""
    insights = []
    if not sales:
        return ["No sales data available yet. Add some sales to see insights."]

    rev_prod = revenue_by_product(sales)
    rev_cat = revenue_by_category(sales)
    rev_reg = revenue_by_region(sales)
    rev_month = revenue_by_month(sales)

    best_product = max(rev_prod, key=rev_prod.get)
    best_category = max(rev_cat, key=rev_cat.get)
    best_region = max(rev_reg, key=rev_reg.get)

    insights.append(f"{best_product} generated the highest revenue "
                     f"({format_currency(rev_prod[best_product])}).")
    insights.append(f"{best_category} is the highest-revenue category "
                     f"({format_currency(rev_cat[best_category])}).")
    insights.append(f"{best_region} recorded the highest sales "
                     f"({format_currency(rev_reg[best_region])}).")

    if rev_month:
        best_month = max(rev_month, key=rev_month.get)
        insights.append(f"{best_month} had the highest monthly revenue "
                         f"({format_currency(rev_month[best_month])}).")

    low = low_performing_products(sales)
    if low:
        # STRING JOIN METHOD used meaningfully to build a sentence.
        insights.append("Low-performing products: " + ", ".join(sorted(low)) + ".")

    total_revenue = sum(calc_revenue(s) for s in sales)
    total_units = sum(s["quantity"] for s in sales)
    insights.append(f"Average revenue per unit sold across all sales is "
                     f"{format_currency(total_revenue / total_units)}." if total_units else
                     "No units have been sold yet.")

    return insights


def filter_sales(sales, product="", category="", region="", date=""):
    """Case-insensitive filtering using string methods (.lower()).
    Implemented as a single LIST COMPREHENSION with several
    conditions chained together."""
    product = product.strip().lower()
    category = category.strip().lower()
    region = region.strip().lower()
    date = date.strip().lower()

    return [
        s for s in sales
        if (product == "" or product in s["product"].lower())
        and (category == "" or category == s["category"].lower())
        and (region == "" or region == s["region"].lower())
        and (date == "" or date == s["date"].lower())
    ]


# ---------------------------------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------------------------------

class SalesDataAnalyzer(tk.Tk):

    NAV_ITEMS = (
        "Dashboard",
        "Sales Records",
        "Add Sale",
        "Product Analysis",
        "Category Analysis",
        "Date Analysis",
        "Search & Filter",
        "Business Insights",
        "Sales Target",
        "What-If Simulator",
    )

    def __init__(self):
        super().__init__()
        self.title("SALES DATA ANALYZER")
        self.geometry("1180x700")
        self.minsize(1000, 620)
        self.configure(bg=COLOR_BG_LIGHT)

        # ---- core data ----
        self.sales = build_sample_dataset()   # LIST OF DICTIONARIES
        self.sales_target = 1000000.0         # default monthly target (rupees)

        self._configure_style()
        self._build_layout()
        self.show_frame("Dashboard")

    # ------------------------------------------------------------------
    # STYLE / LAYOUT SCAFFOLDING
    # ------------------------------------------------------------------
    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Treeview", font=FONT_NORMAL, rowheight=26,
                         background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                         background=COLOR_ACCENT, foreground="white")
        style.map("Treeview.Heading", background=[("active", COLOR_ACCENT_DARK)])

        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"),
                         background=COLOR_ACCENT, foreground="white", padding=8)
        style.map("Accent.TButton", background=[("active", COLOR_ACCENT_DARK)])

        style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"),
                         background=COLOR_DANGER, foreground="white", padding=8)

        style.configure("TCombobox", padding=4)

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=COLOR_BG, width=210)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="\U0001F4CA SALES\nANALYZER", bg=COLOR_BG,
                 fg="white", font=("Segoe UI", 15, "bold"), justify="left",
                 padx=18, pady=24).pack(anchor="w")

        self.nav_buttons = {}
        for item in self.NAV_ITEMS:
            btn = tk.Button(self.sidebar, text=item, anchor="w", bd=0,
                             font=FONT_NAV, bg=COLOR_BG, fg=COLOR_TEXT_LIGHT,
                             activebackground=COLOR_ACCENT, activeforeground="white",
                             padx=20, pady=10, relief="flat", cursor="hand2",
                             command=lambda i=item: self.show_frame(i))
            btn.pack(fill="x")
            self.nav_buttons[item] = btn

        tk.Label(self.sidebar, text="College Mini-Project\nPython Module 03",
                 bg=COLOR_BG, fg=COLOR_MUTED, font=("Segoe UI", 8),
                 justify="left", padx=18, pady=16).pack(side="bottom", anchor="w")

        # Main content area (rebuilt per screen)
        self.content = tk.Frame(self, bg=COLOR_BG_LIGHT)
        self.content.pack(side="right", fill="both", expand=True)

    def show_frame(self, name):
        for key, btn in self.nav_buttons.items():
            btn.configure(bg=COLOR_ACCENT if key == name else COLOR_BG)

        for widget in self.content.winfo_children():
            widget.destroy()

        builder = {
            "Dashboard": self.build_dashboard,
            "Sales Records": self.build_sales_records,
            "Add Sale": self.build_add_sale,
            "Product Analysis": self.build_product_analysis,
            "Category Analysis": self.build_category_analysis,
            "Date Analysis": self.build_date_analysis,
            "Search & Filter": self.build_search_filter,
            "Business Insights": self.build_business_insights,
            "Sales Target": self.build_sales_target,
            "What-If Simulator": self.build_whatif_simulator,
        }[name]
        builder()

    # Convenience: consistent page header
    def _page_header(self, parent, title):
        tk.Label(parent, text=title, font=FONT_TITLE, bg=COLOR_BG_LIGHT,
                 fg="#0f172a").pack(anchor="w", padx=24, pady=(20, 10))

    def _embed_figure(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)
        return canvas

    # ------------------------------------------------------------------
    # 1. DASHBOARD
    # ------------------------------------------------------------------
    def build_dashboard(self):
        self._page_header(self.content, "Dashboard")

        total_revenue = sum(calc_revenue(s) for s in self.sales)
        total_units = sum(s["quantity"] for s in self.sales)
        total_transactions = len(self.sales)
        unique_products = get_unique_products(self.sales)

        units = units_by_product(self.sales)
        best_product = max(units, key=units.get) if units else "N/A"

        cards_frame = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        cards_frame.pack(fill="x", padx=24, pady=(0, 10))

        cards = [
            ("Total Revenue", format_currency(total_revenue), COLOR_ACCENT),
            ("Total Units Sold", str(total_units), COLOR_SUCCESS),
            ("Total Transactions", str(total_transactions), "#9333ea"),
            ("Unique Products", str(len(unique_products)), "#ea580c"),
            ("Best-Selling Product", best_product, "#0891b2"),
        ]
        for label, value, color in cards:
            card = tk.Frame(cards_frame, bg=COLOR_CARD, highlightbackground=color,
                             highlightthickness=2, padx=14, pady=14)
            card.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(card, text=label.upper(), font=FONT_CARD_LABEL, bg=COLOR_CARD,
                     fg=COLOR_MUTED).pack(anchor="w")
            tk.Label(card, text=value, font=FONT_CARD_VALUE, bg=COLOR_CARD,
                     fg=color, wraplength=160, justify="left").pack(anchor="w", pady=(6, 0))

        charts_frame = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        charts_frame.pack(fill="both", expand=True, padx=24, pady=10)

        left = tk.Frame(charts_frame, bg="white", highlightbackground="#cbd5e1", highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = tk.Frame(charts_frame, bg="white", highlightbackground="#cbd5e1", highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))

        rev_cat = revenue_by_category(self.sales)
        fig1, ax1 = plt.subplots(figsize=(4.4, 3.2))
        ax1.bar(rev_cat.keys(), rev_cat.values(), color=COLOR_ACCENT)
        ax1.set_title("Revenue by Category")
        ax1.tick_params(axis='x', rotation=20)
        fig1.tight_layout()
        self._embed_figure(left, fig1)

        rev_prod = revenue_by_product(self.sales)
        fig2, ax2 = plt.subplots(figsize=(4.4, 3.2))
        ax2.pie(rev_prod.values(), labels=rev_prod.keys(), autopct="%1.0f%%",
                textprops={"fontsize": 7})
        ax2.set_title("Revenue Share by Product")
        fig2.tight_layout()
        self._embed_figure(right, fig2)

    # ------------------------------------------------------------------
    # 2. SALES RECORDS
    # ------------------------------------------------------------------
    def build_sales_records(self):
        self._page_header(self.content, "Sales Records")

        toolbar = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        toolbar.pack(fill="x", padx=24)

        ttk.Button(toolbar, text="+ Add Sale", style="Accent.TButton",
                   command=lambda: self.show_frame("Add Sale")).pack(side="left")
        ttk.Button(toolbar, text="Delete Selected", style="Danger.TButton",
                   command=lambda: self._delete_selected(tree)).pack(side="left", padx=8)
        ttk.Button(toolbar, text="Refresh", command=lambda: self.show_frame("Sales Records")
                   ).pack(side="left")

        table_frame = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        table_frame.pack(fill="both", expand=True, padx=24, pady=14)

        tree = ttk.Treeview(table_frame, columns=TABLE_COLUMNS, show="headings")
        for col in TABLE_COLUMNS:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        for idx, s in enumerate(self.sales):
            revenue = calc_revenue(s)
            tree.insert("", "end", iid=str(idx), values=(
                s["date"], s["product"], s["category"], s["quantity"],
                format_currency(s["price"]), s["region"], format_currency(revenue)
            ))

    def _delete_selected(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a record to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete {len(selected)} record(s)?"):
            return
        indices = sorted((int(i) for i in selected), reverse=True)
        for i in indices:
            del self.sales[i]
        self.show_frame("Sales Records")

    # ------------------------------------------------------------------
    # 3. ADD SALE
    # ------------------------------------------------------------------
    def build_add_sale(self):
        self._page_header(self.content, "Add Sale")

        form = tk.Frame(self.content, bg=COLOR_CARD, padx=30, pady=26,
                         highlightbackground="#cbd5e1", highlightthickness=1)
        form.pack(padx=24, pady=10, anchor="nw")

        fields = {}

        def add_row(row, label, widget):
            tk.Label(form, text=label, font=FONT_NORMAL, bg=COLOR_CARD).grid(
                row=row, column=0, sticky="w", pady=8, padx=(0, 12))
            widget.grid(row=row, column=1, pady=8, sticky="ew")

        tk.Label(form, text="Add a New Sale Record", font=FONT_HEADING,
                 bg=COLOR_CARD).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        date_var = tk.StringVar(value=datetime.now().strftime(DATE_FORMAT))
        entry_date = ttk.Entry(form, textvariable=date_var, width=28)
        add_row(1, "Date (dd-mm-yyyy)", entry_date)

        product_var = tk.StringVar()
        combo_product = ttk.Combobox(form, textvariable=product_var, width=26,
                                      values=sorted(PRODUCT_CATALOG.keys()))
        add_row(2, "Product", combo_product)

        category_var = tk.StringVar()
        entry_category = ttk.Entry(form, textvariable=category_var, width=28)
        add_row(3, "Category", entry_category)

        qty_var = tk.StringVar()
        entry_qty = ttk.Entry(form, textvariable=qty_var, width=28)
        add_row(4, "Quantity", entry_qty)

        price_var = tk.StringVar()
        entry_price = ttk.Entry(form, textvariable=price_var, width=28)
        add_row(5, "Price (per unit)", entry_price)

        region_var = tk.StringVar()
        combo_region = ttk.Combobox(form, textvariable=region_var, width=26, values=REGIONS)
        add_row(6, "Region", combo_region)

        def autofill(event=None):
            # Demonstrates looking up a tuple value from the PRODUCT_CATALOG dict.
            chosen = product_var.get().strip()
            if chosen in PRODUCT_CATALOG:
                cat, price = PRODUCT_CATALOG[chosen]
                category_var.set(cat)
                if not price_var.get():
                    price_var.set(str(price))

        combo_product.bind("<<ComboboxSelected>>", autofill)

        status_label = tk.Label(form, text="", font=FONT_NORMAL, bg=COLOR_CARD, fg=COLOR_DANGER)
        status_label.grid(row=8, column=0, columnspan=2, sticky="w", pady=(6, 0))

        def submit():
            date_str = date_var.get().strip()
            product = product_var.get().strip()
            # .upper()/.lower() used meaningfully: normalize category capitalization
            category = category_var.get().strip().title()
            region = region_var.get().strip()

            parsed_date = safe_parse_date(date_str)
            if parsed_date is None:
                status_label.config(text="Invalid date. Use dd-mm-yyyy format.")
                return
            if not product:
                status_label.config(text="Product name cannot be empty.")
                return
            if not category:
                status_label.config(text="Category cannot be empty.")
                return
            if region not in REGIONS:
                status_label.config(text="Please choose a valid region.")
                return
            try:
                quantity = int(qty_var.get().strip())
                price = float(price_var.get().strip())
                if quantity <= 0 or price <= 0:
                    raise ValueError
            except ValueError:
                status_label.config(text="Quantity and Price must be positive numbers.")
                return

            self.sales.append({
                "date": parsed_date.strftime(DATE_FORMAT),
                "product": product,
                "category": category,
                "quantity": quantity,
                "price": price,
                "region": region,
            })
            messagebox.showinfo("Success", f"Sale for '{product}' added successfully!")
            self.show_frame("Dashboard")

        ttk.Button(form, text="Add Sale", style="Accent.TButton",
                   command=submit).grid(row=7, column=0, columnspan=2, sticky="ew", pady=(14, 0))

    # ------------------------------------------------------------------
    # 4. PRODUCT ANALYSIS
    # ------------------------------------------------------------------
    def build_product_analysis(self):
        self._page_header(self.content, "Product Analysis")

        units = units_by_product(self.sales)
        revenue = revenue_by_product(self.sales)

        if not units:
            tk.Label(self.content, text="No data available.", bg=COLOR_BG_LIGHT).pack(padx=24)
            return

        best_selling = max(units, key=units.get)
        highest_revenue = max(revenue, key=revenue.get)
        top5 = top_n_products(self.sales, 5)
        low = low_performing_products(self.sales)

        summary = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        summary.pack(fill="x", padx=24)
        tk.Label(summary, text=f"Best-Selling Product: {best_selling}  ({units[best_selling]} units)",
                 font=FONT_NORMAL, bg=COLOR_BG_LIGHT).pack(anchor="w", pady=2)
        tk.Label(summary, text=f"Highest-Revenue Product: {highest_revenue}  "
                                f"({format_currency(revenue[highest_revenue])})",
                 font=FONT_NORMAL, bg=COLOR_BG_LIGHT).pack(anchor="w", pady=2)
        tk.Label(summary, text="Low-performing products: " + (", ".join(sorted(low)) if low else "None"),
                 font=FONT_NORMAL, bg=COLOR_BG_LIGHT, fg=COLOR_DANGER).pack(anchor="w", pady=2)

        body = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        body.pack(fill="both", expand=True, padx=24, pady=12)

        # Top-5 table
        left = tk.Frame(body, bg="white", highlightbackground="#cbd5e1", highlightthickness=1)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(left, text="Top 5 Products (by units sold)", font=FONT_HEADING,
                 bg="white").pack(anchor="w", padx=10, pady=8)
        for rank, (prod, qty) in enumerate(top5, start=1):
            tk.Label(left, text=f"{rank}. {prod} \u2014 {qty} units", font=FONT_NORMAL,
                     bg="white").pack(anchor="w", padx=20, pady=3)

        # Chart
        right = tk.Frame(body, bg="white", highlightbackground="#cbd5e1", highlightthickness=1)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))
        fig, ax = plt.subplots(figsize=(4.6, 3.4))
        products = list(revenue.keys())
        ax.bar(products, revenue.values(), color="#0891b2")
        ax.set_title("Revenue by Product")
        ax.tick_params(axis='x', rotation=30, labelsize=7)
        fig.tight_layout()
        self._embed_figure(right, fig)

    # ------------------------------------------------------------------
    # 5. CATEGORY ANALYSIS
    # ------------------------------------------------------------------
    def build_category_analysis(self):
        self._page_header(self.content, "Category Analysis")

        categories = get_unique_categories(self.sales)   # SET
        units = units_by_category(self.sales)
        revenue = revenue_by_category(self.sales)

        if not categories:
            tk.Label(self.content, text="No data available.", bg=COLOR_BG_LIGHT).pack(padx=24)
            return

        highest_cat = max(revenue, key=revenue.get)

        info = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        info.pack(fill="x", padx=24)
        tk.Label(info, text=f"Unique Categories ({len(categories)}): {', '.join(sorted(categories))}",
                 font=FONT_NORMAL, bg=COLOR_BG_LIGHT).pack(anchor="w", pady=2)
        tk.Label(info, text=f"Highest-Revenue Category: {highest_cat} "
                             f"({format_currency(revenue[highest_cat])})",
                 font=FONT_NORMAL, bg=COLOR_BG_LIGHT).pack(anchor="w", pady=2)

        body = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        body.pack(fill="both", expand=True, padx=24, pady=12)

        table = ttk.Treeview(body, columns=("Category", "Units", "Revenue"), show="headings", height=6)
        for col in ("Category", "Units", "Revenue"):
            table.heading(col, text=col)
            table.column(col, width=140, anchor="center")
        for cat in sorted(categories):
            table.insert("", "end", values=(cat, units[cat], format_currency(revenue[cat])))
        table.pack(side="left", fill="y", padx=(0, 16))

        fig, ax = plt.subplots(figsize=(5, 3.6))
        ax.bar(revenue.keys(), revenue.values(), color="#9333ea")
        ax.set_title("Category-wise Revenue")
        fig.tight_layout()
        chart_holder = tk.Frame(body, bg="white", highlightbackground="#cbd5e1", highlightthickness=1)
        chart_holder.pack(side="left", fill="both", expand=True)
        self._embed_figure(chart_holder, fig)

    # ------------------------------------------------------------------
    # 6. DATE ANALYSIS
    # ------------------------------------------------------------------
    def build_date_analysis(self):
        self._page_header(self.content, "Date Analysis")

        by_date = revenue_by_date(self.sales)
        by_month = revenue_by_month(self.sales)

        top_frame = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        top_frame.pack(fill="x", padx=24)

        if by_date:
            highest_day = max(by_date, key=by_date.get)
            lowest_day = min(by_date, key=by_date.get)
            tk.Label(top_frame, text=f"Highest Sales Day: {highest_day} "
                                      f"({format_currency(by_date[highest_day])})",
                     font=FONT_NORMAL, bg=COLOR_BG_LIGHT).pack(anchor="w", pady=2)
            tk.Label(top_frame, text=f"Lowest Sales Day: {lowest_day} "
                                      f"({format_currency(by_date[lowest_day])})",
                     font=FONT_NORMAL, bg=COLOR_BG_LIGHT).pack(anchor="w", pady=2)

        # Selected date lookup
        lookup_frame = tk.Frame(self.content, bg=COLOR_CARD, padx=16, pady=12,
                                 highlightbackground="#cbd5e1", highlightthickness=1)
        lookup_frame.pack(fill="x", padx=24, pady=12)
        tk.Label(lookup_frame, text="Check revenue for a specific date (dd-mm-yyyy):",
                 font=FONT_NORMAL, bg=COLOR_CARD).pack(side="left")
        date_entry_var = tk.StringVar()
        entry = ttk.Entry(lookup_frame, textvariable=date_entry_var, width=16)
        entry.pack(side="left", padx=10)
        result_label = tk.Label(lookup_frame, text="", font=("Segoe UI", 10, "bold"),
                                 bg=COLOR_CARD, fg=COLOR_ACCENT)
        result_label.pack(side="left", padx=10)

        def lookup():
            d = date_entry_var.get().strip()
            parsed = safe_parse_date(d)
            if not parsed:
                result_label.config(text="Invalid date format.", fg=COLOR_DANGER)
                return
            key = parsed.strftime(DATE_FORMAT)
            total = by_date.get(key, 0)
            result_label.config(text=f"Revenue on {key}: {format_currency(total)}", fg=COLOR_ACCENT)

        ttk.Button(lookup_frame, text="Check", style="Accent.TButton", command=lookup).pack(side="left")

        # Monthly summary chart
        chart_frame = tk.Frame(self.content, bg="white", highlightbackground="#cbd5e1", highlightthickness=1)
        chart_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        tk.Label(chart_frame, text="Monthly Sales Summary", font=FONT_HEADING,
                 bg="white").pack(anchor="w", padx=10, pady=8)
        if by_month:
            # Sort months chronologically using datetime parsing of the key.
            ordered = sorted(by_month.items(), key=lambda kv: datetime.strptime(kv[0], "%B %Y"))
            months = [m for m, _ in ordered]
            values = [v for _, v in ordered]
            fig, ax = plt.subplots(figsize=(7.5, 3))
            ax.plot(months, values, marker="o", color=COLOR_ACCENT)
            ax.set_title("Revenue by Month")
            ax.tick_params(axis='x', rotation=30, labelsize=8)
            fig.tight_layout()
            self._embed_figure(chart_frame, fig)

    # ------------------------------------------------------------------
    # 7. SEARCH & FILTER
    # ------------------------------------------------------------------
    def build_search_filter(self):
        self._page_header(self.content, "Search & Filter")

        bar = tk.Frame(self.content, bg=COLOR_CARD, padx=16, pady=14,
                        highlightbackground="#cbd5e1", highlightthickness=1)
        bar.pack(fill="x", padx=24)

        product_var = tk.StringVar()
        category_var = tk.StringVar()
        region_var = tk.StringVar()
        date_var = tk.StringVar()

        tk.Label(bar, text="Product", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=0, column=0, padx=6)
        ttk.Entry(bar, textvariable=product_var, width=16).grid(row=1, column=0, padx=6)

        tk.Label(bar, text="Category", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=0, column=1, padx=6)
        ttk.Combobox(bar, textvariable=category_var, width=14,
                     values=sorted(get_unique_categories(self.sales))).grid(row=1, column=1, padx=6)

        tk.Label(bar, text="Region", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=0, column=2, padx=6)
        ttk.Combobox(bar, textvariable=region_var, width=14, values=REGIONS).grid(row=1, column=2, padx=6)

        tk.Label(bar, text="Date (dd-mm-yyyy)", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=0, column=3, padx=6)
        ttk.Entry(bar, textvariable=date_var, width=16).grid(row=1, column=3, padx=6)

        result_frame = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        result_frame.pack(fill="both", expand=True, padx=24, pady=14)

        tree = ttk.Treeview(result_frame, columns=TABLE_COLUMNS, show="headings")
        for col in TABLE_COLUMNS:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")
        vsb = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        count_label = tk.Label(self.content, text="", font=FONT_NORMAL, bg=COLOR_BG_LIGHT)
        count_label.pack(anchor="w", padx=24, pady=(0, 8))

        def run_search():
            for row in tree.get_children():
                tree.delete(row)
            results = filter_sales(self.sales, product_var.get(), category_var.get(),
                                    region_var.get(), date_var.get())
            for s in results:
                revenue = calc_revenue(s)
                tree.insert("", "end", values=(s["date"], s["product"], s["category"],
                                                s["quantity"], format_currency(s["price"]),
                                                s["region"], format_currency(revenue)))
            count_label.config(text=f"{len(results)} record(s) found.")

        ttk.Button(bar, text="Search", style="Accent.TButton", command=run_search).grid(
            row=1, column=4, padx=12)
        ttk.Button(bar, text="Clear", command=lambda: (
            product_var.set(""), category_var.set(""), region_var.set(""),
            date_var.set(""), run_search())).grid(row=1, column=5, padx=6)

        run_search()

    # ------------------------------------------------------------------
    # 8. BUSINESS INSIGHTS
    # ------------------------------------------------------------------
    def build_business_insights(self):
        self._page_header(self.content, "Business Insights")

        card = tk.Frame(self.content, bg=COLOR_CARD, padx=24, pady=20,
                         highlightbackground="#cbd5e1", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=24, pady=10)

        tk.Label(card, text="BUSINESS INSIGHTS", font=FONT_HEADING, bg=COLOR_CARD,
                 fg=COLOR_ACCENT).pack(anchor="w", pady=(0, 12))

        insights = generate_business_insights(self.sales)
        for text in insights:
            row = tk.Frame(card, bg=COLOR_CARD)
            row.pack(fill="x", pady=5)
            tk.Label(row, text="\u2022", font=("Segoe UI", 12, "bold"), bg=COLOR_CARD,
                     fg=COLOR_ACCENT).pack(side="left", padx=(0, 8))
            tk.Label(row, text=text, font=FONT_NORMAL, bg=COLOR_CARD, wraplength=820,
                     justify="left").pack(side="left", anchor="w")

    # ------------------------------------------------------------------
    # 9. SALES TARGET
    # ------------------------------------------------------------------
    def build_sales_target(self):
        self._page_header(self.content, "Sales Target")

        card = tk.Frame(self.content, bg=COLOR_CARD, padx=26, pady=22,
                         highlightbackground="#cbd5e1", highlightthickness=1)
        card.pack(padx=24, pady=10, anchor="nw", fill="x")

        tk.Label(card, text="Monthly Sales Target", font=FONT_HEADING,
                 bg=COLOR_CARD).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        tk.Label(card, text="Set Target Amount (\u20b9):", font=FONT_NORMAL,
                 bg=COLOR_CARD).grid(row=1, column=0, sticky="w", pady=6)
        target_var = tk.StringVar(value=str(int(self.sales_target)))
        ttk.Entry(card, textvariable=target_var, width=20).grid(row=1, column=1, sticky="w", pady=6)

        result_box = tk.Frame(card, bg=COLOR_CARD)
        result_box.grid(row=3, column=0, columnspan=2, sticky="w", pady=(16, 0))

        def calculate():
            try:
                target = float(target_var.get())
                if target <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Target", "Please enter a positive number.")
                return
            self.sales_target = target
            current_sales = sum(calc_revenue(s) for s in self.sales)
            progress = min(current_sales / target * 100, 100)
            remaining = max(target - current_sales, 0)

            for w in result_box.winfo_children():
                w.destroy()

            tk.Label(result_box, text=f"Monthly Target: {format_currency(target)}",
                     font=FONT_NORMAL, bg=COLOR_CARD).pack(anchor="w", pady=2)
            tk.Label(result_box, text=f"Current Sales: {format_currency(current_sales)}",
                     font=FONT_NORMAL, bg=COLOR_CARD).pack(anchor="w", pady=2)
            tk.Label(result_box, text=f"Progress: {progress:.1f}%",
                     font=("Segoe UI", 10, "bold"), bg=COLOR_CARD,
                     fg=COLOR_SUCCESS if progress >= 100 else COLOR_ACCENT).pack(anchor="w", pady=2)
            tk.Label(result_box, text=f"Remaining: {format_currency(remaining)}",
                     font=FONT_NORMAL, bg=COLOR_CARD).pack(anchor="w", pady=2)

            bar_bg = tk.Frame(result_box, bg="#e2e8f0", width=400, height=20)
            bar_bg.pack(anchor="w", pady=(10, 4))
            bar_bg.pack_propagate(False)
            fill_width = int(400 * (progress / 100))
            tk.Frame(bar_bg, bg=COLOR_SUCCESS if progress >= 100 else COLOR_ACCENT,
                     width=fill_width, height=20).place(x=0, y=0)

            status = "\u2705 Target Achieved!" if current_sales >= target else "\u23f3 Target Not Yet Achieved"
            tk.Label(result_box, text=status, font=("Segoe UI", 11, "bold"), bg=COLOR_CARD,
                     fg=COLOR_SUCCESS if current_sales >= target else COLOR_DANGER).pack(anchor="w", pady=(6, 0))

        ttk.Button(card, text="Calculate Progress", style="Accent.TButton",
                   command=calculate).grid(row=2, column=0, columnspan=2, sticky="w", pady=6)

        calculate()

    # ------------------------------------------------------------------
    # 10. WHAT-IF SIMULATOR
    # ------------------------------------------------------------------
    def build_whatif_simulator(self):
        self._page_header(self.content, "What-If Sales Simulator")

        note = tk.Label(self.content, text="This is a projection tool only \u2014 it never "
                         "modifies your actual sales data.", font=("Segoe UI", 9, "italic"),
                         bg=COLOR_BG_LIGHT, fg=COLOR_MUTED)
        note.pack(anchor="w", padx=24)

        container = tk.Frame(self.content, bg=COLOR_BG_LIGHT)
        container.pack(fill="both", expand=True, padx=24, pady=14)

        # ---- Scenario 1: single product projection ----
        card1 = tk.Frame(container, bg=COLOR_CARD, padx=22, pady=18,
                          highlightbackground="#cbd5e1", highlightthickness=1)
        card1.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(card1, text="Single Product Projection", font=FONT_HEADING,
                 bg=COLOR_CARD).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        product_var = tk.StringVar()
        qty_var = tk.StringVar()
        price_var = tk.StringVar()

        tk.Label(card1, text="Product", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(card1, textvariable=product_var, values=sorted(PRODUCT_CATALOG.keys()),
                     width=22).grid(row=1, column=1, pady=6)

        tk.Label(card1, text="Expected Quantity", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(card1, textvariable=qty_var, width=24).grid(row=2, column=1, pady=6)

        tk.Label(card1, text="Expected Price", bg=COLOR_CARD, font=FONT_NORMAL).grid(row=3, column=0, sticky="w", pady=6)
        ttk.Entry(card1, textvariable=price_var, width=24).grid(row=3, column=1, pady=6)

        result1 = tk.Label(card1, text="", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT)
        result1.grid(row=5, column=0, columnspan=2, sticky="w", pady=(12, 0))

        def simulate_single():
            try:
                qty = float(qty_var.get())
                price = float(price_var.get())
                if qty <= 0 or price <= 0:
                    raise ValueError
            except ValueError:
                result1.config(text="Enter valid positive numbers.", fg=COLOR_DANGER)
                return
            projected = qty * price
            result1.config(text=f"Projected Revenue for {product_var.get() or 'product'}: "
                                 f"{format_currency(projected)}", fg=COLOR_ACCENT)

        ttk.Button(card1, text="Simulate", style="Accent.TButton",
                   command=simulate_single).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # ---- Scenario 2: overall percentage increase ----
        card2 = tk.Frame(container, bg=COLOR_CARD, padx=22, pady=18,
                          highlightbackground="#cbd5e1", highlightthickness=1)
        card2.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(card2, text="Overall Sales Growth Projection", font=FONT_HEADING,
                 bg=COLOR_CARD).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        current_total = sum(calc_revenue(s) for s in self.sales)
        tk.Label(card2, text=f"Current Total Sales: {format_currency(current_total)}",
                 font=FONT_NORMAL, bg=COLOR_CARD).grid(row=1, column=0, columnspan=2, sticky="w", pady=6)

        percent_var = tk.StringVar(value="10")
        tk.Label(card2, text="Expected Increase (%)", bg=COLOR_CARD, font=FONT_NORMAL).grid(
            row=2, column=0, sticky="w", pady=6)
        ttk.Entry(card2, textvariable=percent_var, width=24).grid(row=2, column=1, pady=6)

        result2 = tk.Label(card2, text="", font=("Segoe UI", 11, "bold"), bg=COLOR_CARD, fg=COLOR_ACCENT)
        result2.grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 0))

        def simulate_growth():
            try:
                pct = float(percent_var.get())
            except ValueError:
                result2.config(text="Enter a valid percentage.", fg=COLOR_DANGER)
                return
            projected = current_total * (1 + pct / 100)
            result2.config(
                text=f"If sales increase by {pct:.1f}%, Projected Sales: {format_currency(projected)}",
                fg=COLOR_SUCCESS)

        ttk.Button(card2, text="Simulate Growth", style="Accent.TButton",
                   command=simulate_growth).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = SalesDataAnalyzer()
    app.mainloop()