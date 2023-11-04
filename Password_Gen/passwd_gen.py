# Import modules
import random
import string
import flet
from flet import *
import pyperclip


def main(page:Page):

      #! Password Defining the dimensions of the main screen
      page.title = "Password Generator"
      page.horizontal_alignment = "center"
      page.theme_mode = "light"
      page.window_maximizable = False
      page.window_height = 600
      page.window_width = 00
      page.window_max_height=600
      page.window_max_width = 400
      page.window_min_width=400
      page.window_min_height = 600
     

      def passwd(e):
      # Prompt user for password length
        password_length = int(user_input.content.value)
        global password
        password= ""

        # Define possible characters
        characters = string.ascii_letters + string.digits + string.punctuation

        # Generate password
        for i in range(password_length):
            password += random.choice(characters)

        # Print password
        
        passwd_con.content.value = password
        passwd_con.visible = True
        copy_btn.visible = True
        page.update()

        print("Your password is: " + password)

      def copy(e):
          text_to_copy = password
          pyperclip.copy(text_to_copy)
          

      #! Header of the page
      headline = Text(value="Password Generator",
                   font_family="Roboto",size=30,
                   text_align="center",
                   weight="bold"
                   
                   )
      page.add(headline)
      
      #! taking the input from the user
      user_input = Container(
            content = TextField(
            label="Enter the length of your password",
            border_radius=20,
      ),
            padding=30
      )
      #! generate button to generate passwords
      generate_button = Container(
            content = ElevatedButton(
            text = "Generate",
            bgcolor="blue",
            color = "white",
            on_click=passwd
            ),
            
      )
        
      #! password container
      passwd_con = Container(
                  content = Text(
                        value="Nil",
                        color = "white",
                        text_align="center",
                        selectable= True,
                        size= 20
                        
                  ),
            padding=20,
            margin=20,
            visible=False,
            bgcolor="blue",
            border_radius=20
      )
      #! copy button
      copy_btn = ElevatedButton(
            text = "Copy",
            bgcolor="blue",
            color = "white",
            on_click=copy,
            visible=False
      )

      #! managin all the containers in one single column
      column = Column(
            controls = [
                  user_input, generate_button,passwd_con,copy_btn
            ],horizontal_alignment="center"
           
      )
      page.add(column)
      
flet.app(target=main)
