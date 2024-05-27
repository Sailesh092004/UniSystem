import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3
import datetime


class EquipLend:
    def __init__(self):
        self.conn = sqlite3.connect('equipment.db')
        self.create_tables()

        self.root = tk.Tk()
        self.root.title("Equipment Lending and Rental System")

        description_label = tk.Label(self.root,
                                     text="Welcome to the Equipment Lending and Rental System!\nPlease select an option below:",
                                     font=("Arial", 16))
        description_label.pack(pady=10)

        login_button = tk.Button(self.root, text="Login", font=("Arial", 16), width=10, command=self.open_login_frame)
        login_button.pack(pady=5)

        signup_button = tk.Button(self.root, text="Sign Up", font=("Arial", 16), width=10,
                                  command=self.open_signup_frame)
        signup_button.pack(pady=5)

        self.root.mainloop()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            mobile_number TEXT NOT NULL,
                            role TEXT NOT NULL,
                            password TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            id INTEGER PRIMARY KEY,
                            product_name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            condition TEXT NOT NULL,
                            cost_per_day REAL NOT NULL,
                            category TEXT NOT NULL,
                            phone TEXT NOT NULL)''')  # Adding the phone column
        cursor.execute('''CREATE TABLE IF NOT EXISTS rentals (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            item_id INTEGER NOT NULL,
                            start_date DATE NOT NULL,
                            end_date DATE NOT NULL,
                            location TEXT NOT NULL,
                            total_cost REAL NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id),
                            FOREIGN KEY (item_id) REFERENCES items(id))''')
        self.conn.commit()
        cursor.close()

    def open_login_frame(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login Page")

        email_label = tk.Label(login_window, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=5)
        email_entry = tk.Entry(login_window)
        email_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = tk.Label(login_window, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        submit_button = tk.Button(login_window, text="Submit",
                                  command=lambda: self.login(email_entry.get(), password_entry.get()))
        submit_button.grid(row=2, columnspan=2, padx=10, pady=5)

    def open_signup_frame(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up Page")

        name_label = tk.Label(signup_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(signup_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        email_label = tk.Label(signup_window, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5)
        email_entry = tk.Entry(signup_window)
        email_entry.grid(row=1, column=1, padx=10, pady=5)

        mobile_label = tk.Label(signup_window, text="Mobile Number:")
        mobile_label.grid(row=2, column=0, padx=10, pady=5)
        mobile_entry = tk.Entry(signup_window)
        mobile_entry.grid(row=2, column=1, padx=10, pady=5)

        role_label = tk.Label(signup_window, text="Role:")
        role_label.grid(row=3, column=0, padx=10, pady=5)
        role_combobox = ttk.Combobox(signup_window, values=["Student", "Faculty", "Vendor"])
        role_combobox.grid(row=3, column=1, padx=10, pady=5)

        password_label = tk.Label(signup_window, text="Password:")
        password_label.grid(row=4, column=0, padx=10, pady=5)
        password_entry = tk.Entry(signup_window, show="*")
        password_entry.grid(row=4, column=1, padx=10, pady=5)

        confirm_password_label = tk.Label(signup_window, text="Confirm Password:")
        confirm_password_label.grid(row=5, column=0, padx=10, pady=5)
        confirm_password_entry = tk.Entry(signup_window, show="*")
        confirm_password_entry.grid(row=5, column=1, padx=10, pady=5)

        submit_button = tk.Button(signup_window, text="Submit",
                                  command=lambda: self.signup(name_entry.get(), email_entry.get(), mobile_entry.get(),
                                                              role_combobox.get(), password_entry.get(),
                                                              confirm_password_entry.get()))
        submit_button.grid(row=6, columnspan=2, padx=10, pady=5)

    def login(self, email, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + user[1] + "!")
            self.open_welcome_frame(user[1])
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def signup(self, name, email, mobile_number, role, password, confirm_password):
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (name, email, mobile_number, role, password) VALUES (?, ?, ?, ?, ?)",
                       (name, email, mobile_number, role, password))
        self.conn.commit()
        cursor.close()
        messagebox.showinfo("Sign Up Successful", "Account created successfully!")

    def open_welcome_frame(self, user_name):
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome")

        greeting_label = tk.Label(welcome_window, text="Welcome, " + user_name + "!", font=("Arial", 16))
        greeting_label.pack(pady=10)

        question_label = tk.Label(welcome_window, text="Are you looking to lend or borrow?", font=("Arial", 14))
        question_label.pack(pady=5)

        lend_button = tk.Button(welcome_window, text="Lend", font=("Arial", 14), width=10,
                                command=self.open_lend_items_page)
        lend_button.pack(pady=5)

        borrow_button = tk.Button(welcome_window, text="Borrow", font=("Arial", 14), width=10,
                                  command=self.open_borrow_frame)
        borrow_button.pack(pady=5)

        return_button = tk.Button(welcome_window, text="Return", font=("Arial", 14), width=10,
                                  command=self.open_return_frame)
        return_button.pack(pady=5)

    def open_lend_items_page(self):
        lend_window = tk.Toplevel(self.root)
        lend_window.title("Lend a Product")

        product_name_label = tk.Label(lend_window, text="Product Name:")
        product_name_label.grid(row=0, column=0, padx=10, pady=5)
        product_name_entry = tk.Entry(lend_window)
        product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        description_label = tk.Label(lend_window, text="Description:")
        description_label.grid(row=1, column=0, padx=10, pady=5)
        description_entry = tk.Entry(lend_window)
        description_entry.grid(row=1, column=1, padx=10, pady=5)

        condition_label = tk.Label(lend_window, text="Condition:")
        condition_label.grid(row=2, column=0, padx=10, pady=5)
        condition_entry = tk.Entry(lend_window)
        condition_entry.grid(row=2, column=1, padx=10, pady=5)

        cost_label = tk.Label(lend_window, text="Cost per day:")
        cost_label.grid(row=3, column=0, padx=10, pady=5)
        cost_entry = tk.Entry(lend_window)
        cost_entry.grid(row=3, column=1, padx=10, pady=5)

        category_label = tk.Label(lend_window, text="Category:")
        category_label.grid(row=4, column=0, padx=10, pady=5)
        category_combobox = ttk.Combobox(lend_window,
                                         values=["Electronics", "Mobility", "Books", "Hardware Tools", "Stationary",
                                                 "Sports Gear"])
        category_combobox.grid(row=4, column=1, padx=10, pady=5)

        phone_label = tk.Label(lend_window, text="Phone Number:")
        phone_label.grid(row=5, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(lend_window)
        phone_entry.grid(row=5, column=1, padx=10, pady=5)

        submit_button = tk.Button(lend_window, text="Submit",
                                  command=lambda: self.submit_lend_items(product_name_entry.get(),
                                                                         description_entry.get(), condition_entry.get(),
                                                                         cost_entry.get(), category_combobox.get(),
                                                                         phone_entry.get()))
        submit_button.grid(row=6, columnspan=2, padx=10, pady=5)

    def submit_lend_items(self, product_name, description, condition, cost, category, phone):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO items (product_name, description, condition, cost_per_day, category, phone) VALUES (?, ?, ?, ?, ?, ?)",
            (product_name, description, condition, cost, category, phone))
        self.conn.commit()
        cursor.close()
        messagebox.showinfo("Lend Item", "Item added successfully!")

    def open_borrow_frame(self):
        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Borrow Items")

        search_label = tk.Label(borrow_window, text="Search for Items")
        search_label.grid(row=0, column=0, padx=10, pady=5)
        search_entry = tk.Entry(borrow_window)
        search_entry.grid(row=0, column=1, padx=10, pady=5)

        search_button = tk.Button(borrow_window, text="Search", command=lambda: self.search_items(search_entry.get()))
        search_button.grid(row=0, column=2, padx=10, pady=5)

    def search_items(self, query):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM items WHERE product_name LIKE ?", ('%' + query + '%',))
        search_results = cursor.fetchall()
        cursor.close()

        if search_results:
            result_window = tk.Toplevel(self.root)
            result_window.title("Search Results")

            results_label = tk.Label(result_window, text="Search Results", font=("Arial", 16))
            results_label.pack(pady=10)

            for item in search_results:
                item_frame = tk.Frame(result_window, padx=10, pady=5)
                item_frame.pack(fill=tk.X)

                left_frame = tk.Frame(item_frame)
                left_frame.pack(side=tk.LEFT)

                right_frame = tk.Frame(item_frame)
                right_frame.pack(side=tk.RIGHT)

                name_label = tk.Label(left_frame, text=f"Product Name: {item[1]}", font=("Arial", 12), anchor=tk.W)
                name_label.pack(fill=tk.X)

                description_label = tk.Label(left_frame, text=f"Description: {item[2]}", font=("Arial", 10),
                                             anchor=tk.W)
                description_label.pack(fill=tk.X)

                cost_label = tk.Label(right_frame, text=f"Cost per day: ${item[4]}", font=("Arial", 12), anchor=tk.E)
                cost_label.pack(fill=tk.X)

                rent_button = tk.Button(right_frame, text="Rent", font=("Arial", 12),
                                        command=lambda id=item[0], name=item[1], cost=item[4],
                                                       phone=item[5]: self.open_rent_frame(id, name, cost, phone))
                rent_button.pack(fill=tk.X)
        else:
            messagebox.showinfo("Search Results", "No items found matching the search query.")
    def open_rent_frame(self, item_id, product_name, cost_per_day, lender_phone):
        rent_window = tk.Toplevel(self.root)
        rent_window.title("Rent Item")

        start_label = tk.Label(rent_window, text="Start Date:")
        start_label.grid(row=0, column=0, padx=10, pady=5)
        start_cal = Calendar(rent_window, selectmode="day", date_pattern='yyyy-mm-dd')
        start_cal.grid(row=0, column=1, padx=10, pady=5)

        end_label = tk.Label(rent_window, text="End Date:")
        end_label.grid(row=1, column=0, padx=10, pady=5)
        end_cal = Calendar(rent_window, selectmode="day", date_pattern='yyyy-mm-dd')
        end_cal.grid(row=1, column=1, padx=10, pady=5)

        location_label = tk.Label(rent_window, text="Delivery Location:")
        location_label.grid(row=2, column=0, padx=10, pady=5)
        location_entry = tk.Entry(rent_window)
        location_entry.grid(row=2, column=1, padx=10, pady=5)

        phone_label = tk.Label(rent_window, text="Lender's Phone:")
        phone_label.grid(row=3, column=0, padx=10, pady=5)
        phone_entry = tk.Entry(rent_window)
        phone_entry.grid(row=3, column=1, padx=10, pady=5)
        phone_entry.insert(0, lender_phone)

        calculate_button = tk.Button(rent_window, text="Calculate Cost",
                                     command=lambda: self.calculate_cost(start_cal.get_date(), end_cal.get_date(),
                                                                         cost_per_day))
        calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        rent_button = tk.Button(rent_window, text="Rent",
                                command=lambda: self.rent_item(item_id, start_cal.get_date(), end_cal.get_date(),
                                                               location_entry.get(), cost_per_day, phone_entry.get()))
        rent_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def calculate_cost(self, start_date, end_date, cost_per_day):
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            days = (end_date - start_date).days + 1
            total_cost = days * cost_per_day
            messagebox.showinfo("Cost Estimation", f"Total Cost: ${total_cost}")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")

    def rent_item(self, item_id, start_date, end_date, location, cost_per_day, phone):
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            days = (end_date - start_date).days + 1
            total_cost = days * cost_per_day

            user_id = 1  # Assuming user is logged in
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO rentals (user_id, item_id, start_date, end_date, location, total_cost) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, item_id, start_date, end_date, location, total_cost))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Rent Item", f"Item rented successfully! Please call the lender at {phone} and arrange pickup location on the specified date.")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")

    def open_return_frame(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Items")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM rentals WHERE user_id=?", (1,))  # Assuming user is logged in
        rented_items = cursor.fetchall()
        cursor.close()

        if rented_items:
            for item in rented_items:
                item_frame = tk.Frame(return_window, padx=10, pady=5)
                item_frame.pack(fill=tk.X)

                item_name_label = tk.Label(item_frame, text=f"Product Name: {item[2]}", font=("Arial", 12))
                item_name_label.pack(anchor=tk.W)

                return_button = tk.Button(item_frame, text="Return",
                                          command=lambda item_id=item[0]: self.return_item(item_id))
                return_button.pack(anchor=tk.E)
        else:
            messagebox.showinfo("No Items", "You have not rented any items.")

    def return_item(self, rental_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM rentals WHERE id=?", (rental_id,))
        self.conn.commit()
        cursor.close()
        messagebox.showinfo("Item Returned", "Item returned successfully!")


if __name__ == "__main__":
    EquipLend()
