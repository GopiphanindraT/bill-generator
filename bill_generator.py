import tkinter as tk
from tkinter import messagebox, ttk


class BillGenerator:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Bill Generator")
        self.root.geometry("750x550")
        self.root.config(bg="#f4f6f9")

        # Variables
        self.customer_name = tk.StringVar()
        self.item_name = tk.StringVar()
        self.item_price = tk.DoubleVar(value=0.0)
        self.item_qty = tk.IntVar(value=1)
        self.items_list = []

        # Title
        title = tk.Label(
            self.root,
            text="BILL GENERATOR",
            font=("Helvetica", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10,
        )
        title.pack(fill=tk.X)

        # --- Top Frame (Customer Details) ---
        top_frame = tk.LabelFrame(
            self.root,
            text=" Customer Details ",
            font=("Helvetica", 10, "bold"),
            bg="#f4f6f9",
            bd=2,
        )
        top_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(
            top_frame,
            text="Customer Name:",
            font=("Helvetica", 10),
            bg="#f4f6f9",
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(
            top_frame,
            textvariable=self.customer_name,
            font=("Helvetica", 10),
            width=30,
        ).grid(row=0, column=1, padx=10, pady=10)

        # --- Middle Frame (Input & Invoice Display) ---
        mid_frame = tk.Frame(self.root, bg="#f4f6f9")
        mid_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        # Left Column: Item Input
        input_frame = tk.LabelFrame(
            mid_frame,
            text=" Add Items ",
            font=("Helvetica", 10, "bold"),
            bg="#f4f6f9",
            bd=2,
        )
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            input_frame, text="Item Name:", font=("Helvetica", 10), bg="#f4f6f9"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(
            input_frame, textvariable=self.item_name, font=("Helvetica", 10)
        ).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(
            input_frame,
            text="Price per Unit:",
            font=("Helvetica", 10),
            bg="#f4f6f9",
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(
            input_frame, textvariable=self.item_price, font=("Helvetica", 10)
        ).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(
            input_frame, text="Quantity:", font=("Helvetica", 10), bg="#f4f6f9"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(
            input_frame, textvariable=self.item_qty, font=("Helvetica", 10)
        ).grid(row=2, column=1, padx=10, pady=10)

        # Add Item Button
        btn_add = tk.Button(
            input_frame,
            text="Add Item",
            command=self.add_item,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 10, "bold"),
            width=15,
        )
        btn_add.grid(row=3, column=0, columnspan=2, pady=15)

        # Right Column: Bill Area Preview
        bill_frame = tk.LabelFrame(
            mid_frame,
            text=" Invoice Preview ",
            font=("Helvetica", 10, "bold"),
            bg="#f4f6f9",
            bd=2,
        )
        bill_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        scrol_y = tk.Scrollbar(bill_frame, orient=tk.VERTICAL)
        self.txt_area = tk.Text(
            bill_frame,
            yscrollcommand=scrol_y.set,
            font=("Courier", 9),
            bg="white",
        )
        scrol_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrol_y.config(command=self.txt_area.yview)
        self.txt_area.pack(fill=tk.BOTH, expand=True)

        # --- Bottom Frame (Action Buttons) ---
        btn_frame = tk.Frame(self.root, bg="#f4f6f9")
        btn_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Button(
            btn_frame,
            text="Generate Bill",
            command=self.generate_bill,
            bg="#2980b9",
            fg="white",
            font=("Helvetica", 11, "bold"),
            width=15,
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_all,
            bg="#e67e22",
            fg="white",
            font=("Helvetica", 11, "bold"),
            width=15,
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            btn_frame,
            text="Exit",
            command=self.root.quit,
            bg="#c0392b",
            fg="white",
            font=("Helvetica", 11, "bold"),
            width=15,
        ).pack(side=tk.RIGHT, padx=10)

        # Initialize text area headers
        self.welcome_bill()

    def welcome_bill(self):
        self.txt_area.delete("1.0", tk.END)
        self.txt_area.insert(tk.END, "\t\tRetail Invoice\n")
        self.txt_area.insert(tk.END, f"\t\tDate: 2026-05-25\n")
        self.txt_area.insert(
            tk.END, f"==============================================\n"
        )
        self.txt_area.insert(
            tk.END, f"{'Product':<18}{'Qty':<8}{'Price':<10}{'Total':<10}\n"
        )
        self.txt_area.insert(
            tk.END, f"==============================================\n"
        )

    def add_item(self):
        name = self.item_name.get().strip()
        try:
            price = self.item_price.get()
            qty = self.item_qty.get()
        except tk.TclError:
            messagebox.showerror(
                "Error", "Please enter valid numerical values."
            )
            return

        if not name:
            messagebox.showerror("Error", "Please enter an item name.")
            return
        if price <= 0 or qty <= 0:
            messagebox.showerror(
                "Error", "Price and Quantity must be greater than zero."
            )
            return

        total_cost = price * qty
        self.items_list.append((name, qty, price, total_cost))

        # Append directly to text area row
        self.txt_area.insert(
            tk.END, f"{name:<18}{qty:<8}{price:<10.2f}{total_cost:<10.2f}\n"
        )

        # Reset item entries
        self.item_name.set("")
        self.item_price.set(0.0)
        self.item_qty.set(1)

    def generate_bill(self):
        if not self.customer_name.get().strip():
            messagebox.showerror("Error", "Please enter Customer Name.")
            return
        if not self.items_list:
            messagebox.showerror("Error", "No items added to the bill.")
            return

        total_bill = sum(item[3] for item in self.items_list)
        tax = total_bill * 0.05  # 5% tax
        final_total = total_bill + tax

        # Add totals to receipt preview
        self.txt_area.insert(
            tk.END, f"==============================================\n"
        )
        self.txt_area.insert(
            tk.END, f"Customer: {self.customer_name.get()}\n"
        )
        self.txt_area.insert(tk.END, f"Subtotal: Rs. {total_bill:.2f}\n")
        self.txt_area.insert(tk.END, f"Tax (5%): Rs. {tax:.2f}\n")
        self.txt_area.insert(
            tk.END,
            f"Total Amount Due: Rs. {final_total:.2f}\n",
        )
        self.txt_area.insert(
            tk.END, f"==============================================\n"
        )
        messagebox.showinfo("Success", "Bill Generated Successfully!")

    def clear_all(self):
        self.customer_name.set("")
        self.items_list.clear()
        self.welcome_bill()


if __name__ == "__main__":
    root = tk.Tk()
    app = BillGenerator(root)
    root.mainloop()
