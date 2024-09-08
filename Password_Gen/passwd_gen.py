import random
import string
import pyperclip
import pickle
import flet as ft

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

    # Define TextField for update dialog
    update_username_input = ft.TextField(label="Username", border_radius=20, width=300)
    update_password_input = ft.TextField(label="Password", border_radius=20, width=300, password=True)

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

        strength_label.value = f"Strength: {check_password_strength(password)}"
        strength_label.visible = True

        passwd_con.visible = True
        copy_btn.visible = True
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
            passwd_con.content = ft.Text(value=password)
        else:
            passwd_con.content = ft.Text(value="*" * len(password))
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

    # Export saved passwords
    def export_passwords(e):
        export_text = "\n".join([f"Username: {username}, Password: {password}" for username, password in saved_passwords])
        pyperclip.copy(export_text)

    # Show update dialog
    def show_update_dialog(username, current_password):
        def update_password(e):
            if update_username_input.value and update_password_input.value:
                global saved_passwords
                for i, (user, pwd) in enumerate(saved_passwords):
                    if user == username:
                        saved_passwords[i] = (update_username_input.value, update_password_input.value)
                        break
                save_passwords()  # Save to file
                print("Updated passwords:", saved_passwords)  # Debugging output
                update_password_table()
                setattr(update_dialog, 'visible', False)
                page.update()

        update_username_input.value = username
        update_password_input.value = current_password

        update_dialog = ft.AlertDialog(
            title="Update Password",
            content=ft.Column(
                controls=[
                    update_username_input,
                    update_password_input,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(text="Update", on_click=update_password),
                            ft.ElevatedButton(text="Cancel", on_click=lambda e: (setattr(update_dialog, 'visible', False), page.update()))
                        ],
                        spacing=10,
                        alignment="center"
                    )
                ],
                spacing=10
            ),
            actions=[
                ft.ElevatedButton(text="Close", on_click=lambda e: (setattr(update_dialog, 'visible', False), page.update()))
            ]
        )

        page.open(update_dialog)

    # Show delete dialog
    def show_delete_dialog(username):
        def delete_password(e):
            nonlocal username
            global saved_passwords
            saved_passwords = [entry for entry in saved_passwords if entry[0] != username]
            save_passwords()  # Save to file
            print("Deleted passwords:", saved_passwords)  # Debugging output
            update_password_table()
            setattr(delete_dialog, 'visible', False)
            page.update()

        delete_dialog = ft.AlertDialog(
            title="Delete Password",
            content=ft.Text(f"Are you sure you want to delete the password for username: {username}?"),
            actions=[
                ft.ElevatedButton(text="Yes", on_click=delete_password),
                ft.ElevatedButton(text="No", on_click=lambda e: (setattr(delete_dialog, 'visible', False), page.update()))
            ]
        )

        page.open(delete_dialog)

    # Update the table with saved passwords
    def update_password_table():
        data_table.rows = []
        filtered_passwords = [entry for entry in saved_passwords if search_input.value.lower() in entry[0].lower()]
        for username, password in filtered_passwords:
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(username)),
                        ft.DataCell(ft.Text(password)),
                        ft.DataCell(ft.Row(
                            controls=[
                                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, u=username, p=password: show_update_dialog(u, p)),
                                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, u=username: show_delete_dialog(u)),
                                ft.IconButton(icon=ft.icons.COPY, on_click=lambda e, p=password: pyperclip.copy(p))
                            ]
                        ))
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
        content=ft.Text(value="", color="white", text_align="center", selectable=True, size=20),
        padding=20,
        margin=0,
        visible=False,
        bgcolor="blue",
        border_radius=20
    )

    copy_btn = ft.ElevatedButton(text="Copy", bgcolor="blue", color="white", on_click=copy, visible=False)

    strength_label = ft.Text(value="", color="white", size=15, visible=False)

    theme_toggle = ft.Switch(label="Dark Mode", on_change=toggle_theme)

    show_password = ft.Switch(label="Show Password", on_change=toggle_password_visibility)

    # Search and Table Column
    search_input = ft.TextField(label="Search", border_radius=20, width=300, on_change=search_passwords)
    export_btn = ft.ElevatedButton(text="Export", on_click=export_passwords)

    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Username")),
            ft.DataColumn(ft.Text("Password")),
            ft.DataColumn(ft.Text("Actions"))
        ],
        rows=[],
        width=500,
        height=300,
        border_radius=10,
        
    )

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
                copy_btn,
                strength_label,
                show_password,
                theme_toggle
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
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                search_input,
                                export_btn
                            ],
                            spacing=10,
                            alignment="center"
                        )
                    ]
                ),
                ft.Column(
                    controls=[
                        data_table
                    ]
                )
            ],
            horizontal_alignment="left",
            spacing=10
        ),
        padding=ft.Padding(left=20, right=20, top=10, bottom=10),
        width=450
    )

    main_row = ft.Row(
        controls=[
            functionalities_container,
            search_save_table_container
        ],
        spacing=40,
        alignment="start"
    )

    full_height_container = ft.Container(
        content=main_row,
        height=page.window_height,
        width=page.window_width,
        padding=0,
        margin=0,
        expand=True
    )

    page.add(full_height_container)

    # Call to update the table on startup
    update_password_table()

ft.app(target=password_generator_page)
