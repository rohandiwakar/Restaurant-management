import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from collections import Counter
#code
class RestaurantDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Robin Cafe - Restaurant Data Insight Dashboard")
        self.root.geometry("800x600")

        # Load the background image
        self.bg_image = Image.open(r"C:\Users\rohan\Downloads\r.image.jpg")
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to display the background image
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create a frame to hold other widgets
        self.frame = tk.Frame(self.root, bg="#add8e6")
        self.frame.place(x=0, y=0, width=800, height=600)

        # Menu data (item name, price)
        self.menu = []

        # Table orders
        self.table_orders = {}  # Format: {table_number: [{"name": item_name, "price": item_price}]}
        self.order_history = []  # Stores all orders for graph generation

        # Title
        title_label = tk.Label(self.frame, text="Robin Cafe - Restaurant Dashboard", font=("Arial", 30, "bold"), bg="#add8e6", fg="#333333")
        title_label.pack(pady=15)

        # Frame for buttons
        button_frame = tk.Frame(self.frame, bg="#add8e6")
        button_frame.pack(pady=15)

        # Buttons
        menu_button = ttk.Button(button_frame, text="Manage Menu", command=self.manage_menu)
        menu_button.grid(row=0, column=0, padx=15, pady=15)

        bill_button = ttk.Button(button_frame, text="Generate Bill", command=self.generate_bill)
        bill_button.grid(row=0, column=1, padx=15, pady=15)

        pay_button = ttk.Button(button_frame, text="Pay Bill", command=self.pay_bill)
        pay_button.grid(row=0, column=2, padx=10, pady=10)

        graph_button = ttk.Button(button_frame, text="View Graphs", command=self.view_graphs)
        graph_button.grid(row=0, column=3, padx=10, pady=10)

    # Remaining methods (manage_menu, add_item, update_item, etc.) go here...
    def manage_menu(self):
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Manage Menu")
        menu_window.geometry("600x400")
        menu_window.configure(bg="#f0f0f0")

        # Labels and Entry Fields
        item_label = tk.Label(menu_window, text="Item Name:", font=("Arial", 15), bg="#f0f0f0", fg="#333333")
        item_label.grid(row=0, column=0, padx=10, pady=10)
        self.item_entry = tk.Entry(menu_window, font=("Arial", 12))
        self.item_entry.grid(row=0, column=1, padx=10, pady=10)

        price_label = tk.Label(menu_window, text="Price (₹):", font=("Arial", 15), bg="#f0f0f0", fg="#333333")
        price_label.grid(row=1, column=0, padx=10, pady=10)
        self.price_entry = tk.Entry(menu_window, font=("Arial", 12))
        self.price_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        add_button = ttk.Button(menu_window, text="Add Item", command=self.add_item)
        add_button.grid(row=2, column=0, padx=10, pady=10)

        update_button = ttk.Button(menu_window, text="Update Item", command=self.update_item)
        update_button.grid(row=2, column=1, padx=10, pady=10)

        delete_button = ttk.Button(menu_window, text="Delete Item", command=self.delete_item)
        delete_button.grid(row=2, column=2, padx=10, pady=10)

        # Menu List Display
        self.menu_listbox = tk.Listbox(menu_window, width=50, height=10)
        self.menu_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=20)
        self.refresh_menu_list()

    def add_item(self):
        item_name = self.item_entry.get().strip()
        item_price = self.price_entry.get().strip()

        if not item_name or not item_price:
            messagebox.showerror("Error", "Please enter both item name and price.")
            return

        try:
            item_price = float(item_price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return

        self.menu.append({"name": item_name, "price": item_price})
        messagebox.showinfo("Success", f"Item '{item_name}' added to the menu!")
        self.refresh_menu_list()

    def update_item(self):
        selected_index = self.menu_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an item to update.")
            return

        item_name = self.item_entry.get().strip()
        item_price = self.price_entry.get().strip()

        if not item_name or not item_price:
            messagebox.showerror("Error", "Please enter both item name and price.")
            return

        try:
            item_price = float(item_price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number.")
            return

        index = selected_index[0]
        self.menu[index] = {"name": item_name, "price": item_price}
        messagebox.showinfo("Success", f"Item updated to '{item_name}' with price ₹{item_price:.2f}!")
        self.refresh_menu_list()

    def delete_item(self):
        selected_index = self.menu_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an item to delete.")
            return

        index = selected_index[0]
        item_name = self.menu[index]["name"]
        del self.menu[index]
        messagebox.showinfo("Success", f"Item '{item_name}' deleted from the menu!")
        self.refresh_menu_list()

    def refresh_menu_list(self):
        self.menu_listbox.delete(0, tk.END)
        for idx, item in enumerate(self.menu):
            self.menu_listbox.insert(tk.END, f"{idx + 1}. {item['name']} - ₹{item['price']:.2f}")

    def generate_bill(self):
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Generate Bill")
        bill_window.geometry("600x400")

        # Table Number Input
        table_label = tk.Label(bill_window, text="Table Number:", font=("Arial", 12))
        table_label.grid(row=0, column=0, padx=10, pady=10)
        self.table_entry = tk.Entry(bill_window, font=("Arial", 12))
        self.table_entry.grid(row=0, column=1, padx=10, pady=10)

        # Menu Listbox for Orders
        order_label = tk.Label(bill_window, text="Select Items to Order:", font=("Arial", 12))
        order_label.grid(row=1, column=0, padx=10, pady=10)
        self.order_listbox = tk.Listbox(bill_window, width=50, height=10, selectmode=tk.MULTIPLE)
        self.order_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        for item in self.menu:
            self.order_listbox.insert(tk.END, f"{item['name']} - ₹{item['price']:.2f}")

        # Buttons
        add_order_button = ttk.Button(bill_window, text="Add Order", command=self.add_order)
        add_order_button.grid(row=3, column=0, padx=10, pady=10)

        view_bill_button = ttk.Button(bill_window, text="View Bill", command=self.view_bill)
        view_bill_button.grid(row=3, column=1, padx=10, pady=10)

    def add_order(self):
        table_number = self.table_entry.get().strip()
        if not table_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid table number.")
            return

        selected_items = self.order_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one item.")
            return

        table_number = int(table_number)
        if table_number not in self.table_orders:
            self.table_orders[table_number] = []

        for index in selected_items:
            selected_item = self.menu[index]
            self.table_orders[table_number].append(selected_item)
            self.order_history.append(selected_item["name"])  # Save the order to history

        messagebox.showinfo("Success", f"Order added to table {table_number}!")

    def view_bill(self):
        bill_text = ""
        total = 0
        for table, orders in self.table_orders.items():
            bill_text += f"Table {table}:\n"
            for order in orders:
                bill_text += f"  {order['name']} - ₹{order['price']:.2f}\n"
                total += order['price']
            bill_text += "\n"
        messagebox.showinfo("Bill", f"{bill_text}\nTotal: ₹{total:.2f}")

    def pay_bill(self):
        table_number = simpledialog.askinteger("Pay Bill", "Enter Table Number:")
        if table_number in self.table_orders:
            del self.table_orders[table_number]
            messagebox.showinfo("Success", f"Bill for table {table_number} has been paid and reset.")
        else:
            messagebox.showerror("Error", "Invalid table number.")

    def view_graphs(self):
        if not self.order_history:
            messagebox.showinfo("No Data", "No orders available for graph generation.")
            return

        item_counts = Counter(self.order_history)

        # Generate Pie Chart
        plt.figure(figsize=(8, 6))
        plt.pie(item_counts.values(), labels=item_counts.keys(), autopct='%1.1f%%', startangle=140)
        plt.title("Most Ordered Items at Robin Cafe")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantDashboard(root)
    root.mainloop()