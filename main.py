import tkinter as tk
from tkinter import messagebox
from database import Database
from channel import *
from message import *
from USER import *
from server import *
from client import *
from database import *

# Remplacez ces valeurs par vos propres informations de connexion à la base de données MySQL
db = Database(host="localhost", user="root", password="Kiko2002=", db_name="my_discord")


class MainApp: # Classe principale de l'application
    def __init__(self, root):
        """
        Constructeur de la classe MainApp qui permet de créer l'interface graphique de l'application et de gérer les événements
        :param root:
        """
        self.root = root
        self.root.title("My Discord")

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=30, pady=30)
        self.login_label_username = tk.Label(self.login_frame, text="Username:")
        self.login_label_username.grid(row=0, column=0, pady=(0, 10))
        self.login_entry_username = tk.Entry(self.login_frame)
        self.login_entry_username.grid(row=0, column=1, pady=(0, 10))

        self.login_label_password = tk.Label(self.login_frame, text="Password:")
        self.login_label_password.grid(row=1, column=0, pady=(0, 10))
        self.login_entry_password = tk.Entry(self.login_frame, show="*")
        self.login_entry_password.grid(row=1, column=1, pady=(0, 10))

        self.button_login = tk.Button(self.login_frame, text="Login", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        self.button_register = tk.Button(self.login_frame, text="Register", command=self.register)
        self.button_register.grid(row=3, column=0, columnspan=2, pady=(10, 0))


    def open_main_window(self):
        # Fermez la fenêtre de connexion
        self.login_frame.pack_forget()

        # Créez et affichez la fenêtre principale
        self.main_window = tk.Frame(self.root)
        self.main_window.pack(padx=30, pady=30)

        self.label_welcome = tk.Label(self.main_window, text="Welcome to My Discord!")
        self.label_welcome.pack(pady=(0, 10))

        self.button_logout = tk.Button(self.main_window, text="Logout", command=self.logout)
        self.button_logout.pack(pady=(10, 0))

        # Ajoutez une Listbox pour afficher les canaux disponibles
        self.listbox_channels = tk.Listbox(self.main_window, width=30)
        self.listbox_channels.pack(side=tk.LEFT, padx=(0, 10))

        # Ajoutez un Text pour afficher les messages du canal sélectionné
        self.text_messages = tk.Text(self.main_window)
        self.text_messages.pack(side=tk.LEFT)

        # Ajoutez un Entry pour permettre à l'utilisateur d'envoyer des messages
        self.entry_message = tk.Entry(self.main_window)
        self.entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def load_channels(self):
            self.listbox_channels.delete(0, tk.END)
            db.cursor.execute("SELECT * FROM channels")
            channels = db.cursor.fetchall()
            for channel in channels:
                self.listbox_channels.insert(tk.END, channel[1])

            self.listbox_channels.bind("<<ListboxSelect>>", self.load_messages)

    def load_messages(self, event):
        selection = self.listbox_channels.curselection()
        if not selection:
            return
        selected_channel = self.listbox_channels.get(selection)
        self.text_messages.delete("1.0", tk.END)

        db.cursor.execute("SELECT * FROM channels WHERE name=%s", (selected_channel,))
        channel = db.cursor.fetchone()

        db.cursor.execute(
            "SELECT messages.content, users.username, messages.timestamp FROM messages JOIN users ON messages.user_id=users.id WHERE messages.channel_id=%s ORDER BY messages.timestamp ASC",
            (channel[0],))
        messages = db.cursor.fetchall()

        for message in messages:
            self.text_messages.insert(tk.END, f"{message[1]} ({message[2].strftime('%m/%d/%Y %H:%M:%S')}):\n")
            self.text_messages.insert(tk.END, f"{message[0]}\n\n")

    def logout(self):
        # Fermez la fenêtre principale et réaffichez la fenêtre de connexion
        self.main_window.pack_forget()
        self.login_frame.pack(padx=30, pady=30)

    def login(self):
        username = self.login_entry_username.get()
        password = self.login_entry_password.get()

        try:
            db.cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = db.cursor.fetchone()

            if user:
                messagebox.showinfo("Login", "Successfully logged in")
                self.open_main_window()  # Ajoutez cette ligne pour ouvrir la fenêtre principale
            else:
                messagebox.showerror("Error", "Invalid username or password")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def register(self):
        self.create_registration_form()

    def create_registration_form(self):
        self.registration_form = tk.Toplevel(self.root)
        self.registration_form.title("Registration")

        self.label_username = tk.Label(self.registration_form, text="Username:")
        self.label_username.pack(pady=(30, 0))
        self.entry_username = tk.Entry(self.registration_form)
        self.entry_username.pack()

        self.label_full_name = tk.Label(self.registration_form, text="Full Name:")
        self.label_full_name.pack(pady=(30, 0))
        self.entry_full_name = tk.Entry(self.registration_form)
        self.entry_full_name.pack()

        self.label_email = tk.Label(self.registration_form, text="Email:")
        self.label_email.pack(pady=(30, 0))
        self.entry_email = tk.Entry(self.registration_form)
        self.entry_email.pack()

        self.label_password = tk.Label(self.registration_form, text="Password:")
        self.label_password.pack(pady=(30, 0))
        self.entry_password = tk.Entry(self.registration_form, show="*")
        self.entry_password.pack()

        self.button_submit = tk.Button(self.registration_form, text="Submit", command=self.submit_registration)
        self.button_submit.pack(pady=(30, 0))

    def submit_registration(self):
        username = self.entry_username.get()
        full_name = self.entry_full_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        try:
            db.cursor.execute("INSERT INTO users (username, full_name, email, password) VALUES (%s, %s, %s, %s)",
                              (username, full_name, email, password))
            db.conn.commit()
            messagebox.showinfo("Registration", "Successfully registered")
            self.registration_form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()