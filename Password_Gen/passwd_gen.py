import random
import string
import pyperclip
import pickle
import flet as ft
import csv
from flet import TemplateRoute
from io import StringIO

# Global variable to store saved passwords
saved_passwords = []

# Load saved passwords from a file
def load_passwords():
    try:
        with open("passwords.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Save passwords to a file
def save_passwords():
    with open("passwords.pkl", "wb") as file:
        pickle.dump(saved_passwords, file)

# Check password strength
def check_password_strength(password):
    if len(password) < 6:
        return "Weak"
    if len(password) < 10:
        return "Moderate"
    return "Strong"

# Generate password page
def password_generator_page(page: ft.Page):
    page.title = "Password Generator"
    page.horizontal_alignment = "center"
    page.theme_mode = "light"
    page.window_maximizable = False
    page.window_height = 700
    page.window_width = 1200
    page.window_min_width = 1200
    page.window_min_height = 700

    global password
    password = ""

    # Load saved passwords
    global saved_passwords
    saved_passwords = load_passwords()
    print("Loaded passwords:", saved_passwords)  # Debugging output

    # Function to generate a password
    def passwd(e):
        try:
            password_length = int(user_input.value)
        except ValueError:
            password_length = 12

        global password
        password = ""

        characters = string.ascii_lowercase
        if include_uppercase.value:
            characters += string.ascii_uppercase
        if include_digits.value:
            characters += string.digits
        if include_special.value:
            characters += string.punctuation

        for i in range(password_length):
            password += random.choice(characters)

        update_password_visibility()
        strength = check_password_strength(password)
        strength_label.value = f"Strength: {strength}"
        strength_label.visible = True
        if strength == "Strong":
            strength_label.color = "green"
        elif strength == "Moderate":
            strength_label.color = "orange"
            
        else:
            strength_label.color = "red"
        passwd_con.visible = True
        
        page.update()

    # Copy password to clipboard
    def copy(e):
        pyperclip.copy(password)

    # Toggle theme mode
    def toggle_theme(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # Update password visibility based on the toggle state
    def update_password_visibility():
        if show_password.value:
            passwd_con.content = ft.Text(value=password,color="white")
        else:
            passwd_con.content = ft.Text(value="*" * len(password),color="white")
        page.update()

    # Toggle password visibility
    def toggle_password_visibility(e):
        update_password_visibility()

    # Save the password and update the table
    def save_password(e):
        if username_input.value and password:
            global saved_passwords
            saved_passwords.append((username_input.value, password))
            save_passwords()  # Save to file
            print("Saved passwords:", saved_passwords)  # Debugging output
            update_password_table()
            username_input.value = ""
            user_input.value = ""
            page.update()

    # Export saved passwords to CSV
    def export_passwords_csv(e):
        if not saved_passwords:
            page.add(ft.Snackbar(text="No passwords to export!"))
            return
        
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Username", "Password"])
        csv_writer.writerows(saved_passwords)
        
        # Save CSV data to file
        csv_filename = "passwords_export.csv"
        with open(csv_filename, "w", newline="") as csv_file:
            csv_file.write(csv_output.getvalue())
        
        page.add(ft.SnackBar(ft.Text(f"Passwords exported to {csv_filename}!")))

    # Update the table with saved passwords
    def update_password_table():
        data_table.rows = []
        saved_passwords.reverse()
        filtered_passwords = [entry for entry in saved_passwords if search_input.value.lower() in entry[0].lower()]
        for username, password in filtered_passwords:
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(username)),
                        ft.DataCell(ft.Text(password)),
                    ]
                )
            )
        print("Table updated with passwords:", filtered_passwords)  # Debugging output
        page.update()

    # Filter the table based on search input
    def search_passwords(e):
        update_password_table()

    # UI Components for the functionalities column
    headline = ft.Text(value="Password Generator", font_family="Roboto", size=30, text_align="center", weight="bold")

    username_input = ft.TextField(label="Enter Username", border_radius=20, width=300)

    user_input = ft.TextField(label="Enter the length of your password", border_radius=20, width=300)

    include_uppercase = ft.Checkbox(label="Include Uppercase", value=True)
    include_digits = ft.Checkbox(label="Include Digits", value=True)
    include_special = ft.Checkbox(label="Include Special Characters", value=True)

    generate_button = ft.ElevatedButton(text="Generate", bgcolor="blue", color="white", on_click=passwd)

    save_button = ft.ElevatedButton(text="Save Password", on_click=save_password)

    passwd_con = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(value="", color="white", text_align="center", selectable=True, size=20),
                ft.ElevatedButton(text="Copy", bgcolor="blue", color="white", on_click=copy)
            ]
        ),
        padding=20,
        margin=0,
        visible=False,
        bgcolor="blue",
        border_radius=20
    )

    strength_label = ft.Text(value="", color="white", size=15, visible=False)

    theme_toggle = ft.Switch(label="Dark Mode", on_change=toggle_theme)

    show_password = ft.Switch(label="Show Password", on_change=toggle_password_visibility)

    # Search and Table Column
    search_input = ft.TextField(label="Search", border_radius=20, width=300, on_change=search_passwords)
    export_btn_csv = ft.ElevatedButton(text="Export to CSV", on_click=export_passwords_csv)
    
    # New button to redirect to /login
    new_user_button = ft.ElevatedButton(text="Add New User", on_click=lambda _: page.go("/login"))

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Username")),
            ft.DataColumn(ft.Text("Password")),
        ],
        rows=[],
        width=500,
        height=300,
        border_radius=10,
    )
    
    lv = ft.ListView(
        expand=True,
        height=400,  # Fixed height for the ListView
        spacing=10,
        padding=20,
        auto_scroll=True
    )
    lv.controls.append(data_table)

    # Layout Containers
    functionalities_container = ft.Container(
        content=ft.Column(
            controls=[
                headline,
                username_input,
                user_input,
                include_uppercase,
                include_digits,
                include_special,
                ft.Row(
                    controls=[
                        generate_button,
                        save_button
                    ],
                    spacing=10,
                    alignment="start"
                ),
                passwd_con,
                strength_label,
                show_password,
                theme_toggle,
                new_user_button
            ],
            spacing=10,
            alignment="center"
        ),
        padding=ft.Padding(left=60, right=20, top=0, bottom=0),
        width=450
    )

    search_save_table_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        search_input,
                        export_btn_csv
                    ],
                    spacing=10,
                    alignment="center"
                ),
                ft.Column(
                    controls=[lv],
                    scroll=ft.ScrollMode.ALWAYS,
                    height=400
                )
            ],
            horizontal_alignment="left",
            spacing=10
        ),
        padding=ft.Padding(left=20, right=20, top=10, bottom=10),
        width=550,
    )

    main_row = ft.Row(
        controls=[
            functionalities_container,
            search_save_table_container
        ],
        spacing=40,
        alignment="start"
    )
    
    global full_height_container
    full_height_container = ft.Container(
        content=main_row,
        height=page.window_height,
        width=page.window_width,
        padding=0,
        margin=0,
        expand=True
    )

    # Call to update the table on startup
    update_password_table()

    # Route handling
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    controls=[login_page()]
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/",
                    controls=[full_height_container]
                )
            )

    def login_page():
        def save_new_password(e):
            new_username = new_username_input.value
            new_password = new_password_input.value
            if new_username and new_password:
                saved_passwords.append((new_username, new_password))
                save_passwords()
                new_username_input.value = ""
                new_password_input.value = ""
                print("New user added:", (new_username, new_password))  # Debugging output
                page.go("/")
                update_password_table()
        
        headline = ft.Text(value="Add New User", font_family="Roboto", size=30, text_align="center", weight="bold")
        new_username_input = ft.TextField(label="New Username", border_radius=20, width=300)
        new_password_input = ft.TextField(label="New Password", border_radius=20, width=300)
        save_new_user_button = ft.ElevatedButton(text="Save New User", on_click=save_new_password)
        go_back_button = ft.ElevatedButton(text="Go Back", on_click= lambda _:page.go("/"))

        return ft.Column(
            controls=[
                headline,
                new_username_input,
                new_password_input,
                save_new_user_button,
                go_back_button
            ],
            alignment=ft.alignment.center,
            expand=True,
            
            spacing=20
        )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=password_generator_page)
