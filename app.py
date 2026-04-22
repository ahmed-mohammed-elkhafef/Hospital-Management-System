import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from core.SystemManager import SystemManager
import ctypes

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

sys.path.append(os.path.abspath("."))
sys.path.append(resource_path("core"))
sys.path.append(resource_path("model"))


try:
    myappid = 'group2.hospital.management.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

class HospitalApp:
    """
    Main Graphical User Interface (GUI) application class for the Hospital Management System.
    
    This class handles rendering all screens, managing user interactions, 
    and routing data to/from the underlying SystemManager backend.
    """

    def __init__(self, root):
        """
        Initializes the main application window, configures themes, 
        initializes the backend manager, and displays the initial login screen.
        
        Args:
            root (tk.Tk): The main Tkinter root window instance.
        """
        self.manager = SystemManager()
        self.manager.load_data() 
        self.root = root
        self.root.title("Group 2 - Hospital Management System")
        self.root.geometry("1100x750")

        try:
           
            icon_path = resource_path("icon.ico")
            self.root.iconbitmap(icon_path)
            
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not load icon. Error: {e}")

        self.manager = SystemManager()
        self.current_role = None  # Stores 'admin' or 'user' after login
        try:
            self.manager.load_data()
        except:
            pass
        # Color Theme Configuration
        self.bg_color = "#f4f7f6"
        self.sidebar_color = "#2c3e50"
        self.btn_color = "#34495e"
        self.accent_color = "#3498db"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"

        self.show_login_screen()

    def show_login_screen(self):
        """
        Renders the secure login interface. 
        Validates credentials and determines user role (Admin/User).
        """
        self.login_frame = tk.Frame(self.root, bg=self.bg_color)
        self.login_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        center_frame = tk.Frame(self.login_frame, bg="white", padx=40, pady=40, relief="groove", bd=2)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(center_frame, text="🔒 System Login", font=("Segoe UI", 22, "bold"), bg="white").pack(pady=(0, 20))
        
        tk.Label(center_frame, text="Username:", bg="white").pack(anchor="w")
        self.user_ent = tk.Entry(center_frame, width=30, font=("Arial", 12))
        self.user_ent.pack(pady=5)
        self.user_ent.focus_set()
        
        tk.Label(center_frame, text="Password:", bg="white").pack(anchor="w")
        self.pass_ent = tk.Entry(center_frame, width=30, font=("Arial", 12), show="*")
        self.pass_ent.pack(pady=5)

        def attempt_login(event=None):
            user, pw = self.user_ent.get(), self.pass_ent.get()
            if (user == "admin" and pw == "admin123") or (user == "user" and pw == "123456"):
                self.current_role = user
                self.root.unbind('<Return>')
                self.login_frame.destroy()
                self.setup_main_ui()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        self.root.bind('<Return>', attempt_login)
        tk.Button(center_frame, text="Login", command=attempt_login, bg=self.success_color, fg="white", 
                  font=("Arial", 12, "bold"), width=15, pady=8, relief="flat", cursor="hand2").pack(pady=20)

    def setup_main_ui(self):
        """
        Configures the primary layout of the application post-login.
        Sets up the sidebar for navigation and the main content area.
        """
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=220)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(side="right", expand=True, fill="both")
        
        self.header_frame = tk.Frame(self.main_container, bg="white", height=60)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        
        self.page_title_label = tk.Label(self.header_frame, text="Dashboard", font=("Segoe UI", 16, "bold"), bg="white", fg=self.sidebar_color)
        self.page_title_label.pack(side="left", padx=20, pady=15)
        
        self.content_area = tk.Frame(self.main_container, bg=self.bg_color, padx=30, pady=30)
        self.content_area.pack(side="top", expand=True, fill="both")
        
        self.setup_sidebar_buttons()
        self.show_dashboard()

    def setup_sidebar_buttons(self):
        """
        Populates the sidebar with navigation buttons based on the user's role.
        Admin users get access to additional management features.
        """
        tk.Label(self.sidebar, text="🏥 Group 2 HMS", bg=self.sidebar_color, fg="white", font=("Segoe UI", 16, "bold")).pack(pady=20)
        menu = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Add Patient", lambda: self.show_add_form("patient")),
            ("👨‍⚕️ Add Staff", lambda: self.show_add_form("staff")),
            ("🔍 Search", self.show_search),
            ("📋 View Patients", lambda: self.show_all_records("patients")),
            ("📋 View Staff", lambda: self.show_all_records("staff")),
            ("🏢 Departments Info", self.show_departments_view)
        ]
        if self.current_role == "admin": 
            menu.append(("⚙️ Manage Depts", self.show_manage_depts))
            
        menu.append(("🔄 Logout", self.logout))
        
        for text, cmd in menu:
            tk.Button(self.sidebar, text=text, command=cmd, bg=self.btn_color, fg="white",
                      font=("Segoe UI", 10), relief="flat", width=22, pady=10, cursor="hand2").pack(pady=2, padx=10)
                      
        tk.Button(self.sidebar, text="❌ Exit System", command=self.root.quit, bg="#c0392b", fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", width=22, pady=10, cursor="hand2").pack(side="bottom", pady=20, padx=10)

    def clear_content(self, title):
        """
        Clears the main content area to prepare for a new screen and updates the header title.
        
        Args:
            title (str): The text to display in the header bar.
        """
        self.page_title_label.config(text=title)
        for widget in self.content_area.winfo_children(): 
            widget.destroy()

    def show_dashboard(self):
        """Renders the main dashboard containing system-wide statistics with clickable boxes."""
        self.clear_content("📊 System Dashboard")
        depts = self.manager.hospital.departments
        p_count = sum(len(d.patients) for d in depts)
        s_count = sum(len(d.staff) for d in depts)
        
        f = tk.Frame(self.content_area, bg=self.bg_color)
        f.pack(fill="x", pady=20)
        
        self.create_box(f, "Departments", len(depts), "#e67e22", self.show_departments_view)
        self.create_box(f, "Patients", p_count, self.success_color, lambda: self.show_all_records("patients"))
        self.create_box(f, "Staff Members", s_count, self.accent_color, lambda: self.show_all_records("staff"))

    def create_box(self, parent, title, value, color, command):
        """Helper method to create a clickable statistic box for the dashboard."""
        b = tk.Frame(parent, bg=color, width=220, height=130, padx=20, pady=20, cursor="hand2")
        b.pack(side="left", padx=15, expand=True, fill="both")
        b.pack_propagate(False)
        
        b.bind("<Button-1>", lambda e: command())
        
        l1 = tk.Label(b, text=value, font=("Arial", 32, "bold"), bg=color, fg="white", cursor="hand2")
        l1.pack()
        l1.bind("<Button-1>", lambda e: command())
        
        l2 = tk.Label(b, text=title, font=("Arial", 11), bg=color, fg="white", cursor="hand2")
        l2.pack()
        l2.bind("<Button-1>", lambda e: command())

    def show_all_records(self, type):
        """
        Displays a scalable Treeview table showing all active patients or staff members.
        
        Args:
            type (str): Either 'patients' or 'staff' to determine which data to load.
        """
        title = "📋 All Patients List" if type == "patients" else "📋 All Staff List"
        self.clear_content(title)
        
        last_col_name = "Medical Record" if type == "patients" else "Job Position"
        cols = ("ID", "Name", "Age", "Department", last_col_name)
        tree = ttk.Treeview(self.content_area, columns=cols, show="headings")
        # Configure columns and bind the sorting function to the headers
        for col in cols:
            tree.heading(col, text=col, command=lambda c=col: self.sort_tree_column(tree, c, False))
            
            width = 250 if col == last_col_name else 120
            tree.column(col, width=width, anchor="center")
        
        sc = ttk.Scrollbar(self.content_area, orient="vertical", command=tree.yview)
        tree.configure(yscroll=sc.set)
        
        tree.pack(side="left", expand=True, fill="both")
        sc.pack(side="right", fill="y")

        for dept in self.manager.hospital.departments:
            data_list = dept.patients if type == "patients" else dept.staff
            for item in data_list:
                extra_info = item.medical_record if type == "patients" else item.position
                tree.insert("", "end", values=(item.person_id, item.name, item.age, dept.name, extra_info))

    def sort_tree_column(self, tree, col, reverse):
        """
        Sorts the Treeview data when a column header is clicked.
        Supports both alphabetical sorting for strings and numerical sorting for numbers.
        
        Args:
            tree (ttk.Treeview): The treeview widget being sorted.
            col (str): The identifier of the column to sort by.
            reverse (bool): Flag indicating whether to sort in descending order.
        """
        # Retrieve all data from the specified column
        data_list = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        # Try to sort numerically (for Age, ID), fallback to alphabetical sorting (for Names)
        try:
            data_list.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            data_list.sort(reverse=reverse)
            
        # Rearrange the items in the Treeview based on the sorted list
        for index, (val, child) in enumerate(data_list):
            tree.move(child, '', index)
            
        # Update the column heading to reverse the sort order on the next click
        tree.heading(col, command=lambda: self.sort_tree_column(tree, col, not reverse))

    def show_add_form(self, mode):
        """
        Renders an input form for adding new entities to the system.
        
        Args:
            mode (str): Determines the form context ('patient' or 'staff').
        """
        self.clear_content("➕ Add New " + mode.capitalize())
        depts = [d.name for d in self.manager.hospital.departments]
        if not depts: 
            messagebox.showwarning("!", "No Departments found!"); return
        
        f = tk.Frame(self.content_area, bg="white", padx=40, pady=40)
        f.pack(pady=10, fill="both")
        
        dept_var = tk.StringVar(value=depts[0])
        tk.Label(f, text="Department:", bg="white").grid(row=0, column=0, pady=10)
        tk.OptionMenu(f, dept_var, *depts).grid(row=0, column=1, padx=20)
        
        tk.Label(f, text="Name:", bg="white").grid(row=1, column=0, pady=10)
        name_ent = tk.Entry(f, width=30); name_ent.grid(row=1, column=1)
        
        tk.Label(f, text="Age:", bg="white").grid(row=2, column=0, pady=10)
        age_ent = tk.Entry(f, width=30); age_ent.grid(row=2, column=1)
        
        extra_lbl = "Record:" if mode == "patient" else "Position:"
        tk.Label(f, text=extra_lbl, bg="white").grid(row=3, column=0, pady=10)
        extra_ent = tk.Entry(f, width=30); extra_ent.grid(row=3, column=1)

        def save():
            if mode == "patient": 
                res = self.manager.add_patient(dept_var.get(), name_ent.get(), int(age_ent.get()), extra_ent.get())
            else: 
                res = self.manager.add_staff(dept_var.get(), name_ent.get(), int(age_ent.get()), extra_ent.get())
            messagebox.showinfo("Done", res)
            self.show_dashboard()
            
        tk.Button(self.content_area, text="Save", command=save, bg=self.success_color, fg="white", width=20, pady=10).pack(pady=20)

    def show_search(self):
        """Displays a search bar and a text area to render matched patient/staff results."""
        self.clear_content("🔍 Search & Records")
        sf = tk.Frame(self.content_area, bg=self.bg_color)
        sf.pack(fill="x", pady=10)
        
        ent = tk.Entry(sf, width=40, font=("Arial", 12))
        ent.pack(side="left", padx=10)
        
        txt = tk.Text(self.content_area, height=18, width=95, font=("Consolas", 11), bg="#fff")
        txt.pack(pady=10)
        
        def run():
            res = self.manager.search_person_by_name(ent.get())
            txt.delete("1.0", tk.END)
            txt.insert(tk.END, res)
            
        tk.Button(sf, text="Search", command=run, bg=self.accent_color, fg="white", width=12).pack(side="left")

    def show_departments_view(self):
        """
        Renders a scrollable view showing all hospital departments.
        Ensures all department cards are visible regardless of window size.
        """
        self.clear_content("🏥 Hospital Departments")

        canvas = tk.Canvas(self.content_area, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, dept in enumerate(self.manager.hospital.departments):
            card = tk.Frame(scrollable_frame, bg="white", relief="groove", bd=2, padx=20, pady=20)
            card.grid(row=i // 3, column=i % 3, padx=15, pady=15, sticky="nsew")
            
            tk.Label(card, text=dept.name, font=("Segoe UI", 12, "bold"), bg="white").pack()
            tk.Label(card, text=f"Staff: {len(dept.staff)}", bg="white", fg="gray").pack()
            
            tk.Button(card, text="View Staff", bg=self.accent_color, fg="white", 
                      command=lambda d=dept: self.view_dept_staff(d), cursor="hand2").pack(pady=10)

    def view_dept_staff(self, dept):
        """
        Displays a table of staff members belonging to a specific department.
        Includes automatic sorting when column headers are clicked.
        """
        self.clear_content(f"👨‍⚕️ Staff in {dept.name}")
        
        cols = ("ID", "Name", "Age", "Position")
        tree = ttk.Treeview(self.content_area, columns=cols, show="headings")
        
        for col in cols:
            tree.heading(col, text=col, command=lambda c=col: self.sort_tree_column(tree, c, False))
            tree.column(col, anchor="center", width=150)
            
        for s in dept.staff:
            tree.insert("", "end", values=(s.person_id, s.name, s.age, s.position))
            
        tree.pack(expand=True, fill="both")
        
        tk.Button(self.content_area, text="⬅️ Back to Departments", 
                  command=self.show_departments_view, bg=self.btn_color, fg="white", 
                  pady=5, padx=15, cursor="hand2").pack(pady=10)

    def show_manage_depts(self):
        """Renders the department management UI (Admin only) to add or safely delete departments."""
        self.clear_content("⚙️ Manage Departments")
        
        # Add Department
        af = tk.LabelFrame(self.content_area, text="Add Dept", padx=20, pady=20, bg="white")
        af.pack(fill="x", pady=10)
        e = tk.Entry(af, width=40); e.pack(side="left", padx=10)
        
        def add(): 
            self.manager.add_department(e.get())
            self.show_manage_depts()
            
        tk.Button(af, text="Add", command=add, bg=self.success_color, fg="white").pack(side="left")
        
        # Delete Department
        depts = [d.name for d in self.manager.hospital.departments]
        if depts:
            df = tk.LabelFrame(self.content_area, text="Delete Dept", padx=20, pady=20, bg="white")
            df.pack(fill="x", pady=20)
            v = tk.StringVar(value=depts[0])
            tk.OptionMenu(df, v, *depts).pack(side="left", padx=10)
            
            def delete(): 
                self.manager.remove_department(v.get())
                self.show_manage_depts()
                
            tk.Button(df, text="Delete", command=delete, bg=self.danger_color, fg="white").pack(side="left")

    def logout(self):
        """Clears the main window and redirects the user back to the login screen."""
        for w in self.root.winfo_children(): 
            w.destroy()
        self.show_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x750")
    app = HospitalApp(root)
    root.mainloop()