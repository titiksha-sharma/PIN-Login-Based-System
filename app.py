import flet as ft    # pyright: ignore[reportMissingImports]
import random
import string
import sys
import io
import os

# FORCE REAL-TIME TERMINAL OUTPUT - This is the ULTIMATE FIX
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
os.environ['PYTHONUNBUFFERED'] = '1'

# Windows specific real-time fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)

def generate_new_pin():
    """Generate a random 4-digit PIN."""
    new_pin = ''.join(random.choices(string.digits, k=4))
    print(f"New PIN generated: {new_pin}", flush=True)
    sys.stdout.flush()
    return new_pin

def main(page: ft.Page):
    page.title = "Trial"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50
    page.update()

    # Current PIN - starts with default
    current_pin = "1234"
    print(f"Initial PIN: {current_pin}", flush=True)
    sys.stdout.flush()

    def show_login_view():
        nonlocal current_pin
        
        # Clear any existing PIN input
        page.controls.clear()
        
        pin_text = ft.TextField(
            label="Enter PIN",
            password=True,
            can_reveal_password=True,
            width=250,
            text_align=ft.TextAlign.CENTER,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]")
        )
        
        def number_click(e):
            if len(pin_text.value) < 4:
                pin_text.value += e.control.data
                pin_text.update()
                
        
        def clear_pin(e):
            pin_text.value = ""
            pin_text.update()
            
        
        # Number buttons
        keypad_row1 = ft.Row([
            ft.ElevatedButton("1", width=80, height=60, on_click=number_click, data="1"),
            ft.ElevatedButton("2", width=80, height=60, on_click=number_click, data="2"),
            ft.ElevatedButton("3", width=80, height=60, on_click=number_click, data="3"),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        keypad_row2 = ft.Row([
            ft.ElevatedButton("4", width=80, height=60, on_click=number_click, data="4"),
            ft.ElevatedButton("5", width=80, height=60, on_click=number_click, data="5"),
            ft.ElevatedButton("6", width=80, height=60, on_click=number_click, data="6"),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        keypad_row3 = ft.Row([
            ft.ElevatedButton("7", width=80, height=60, on_click=number_click, data="7"),
            ft.ElevatedButton("8", width=80, height=60, on_click=number_click, data="8"),
            ft.ElevatedButton("9", width=80, height=60, on_click=number_click, data="9"),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        keypad_row4 = ft.Row([
            ft.ElevatedButton("", width=80, height=60),
            ft.ElevatedButton("0", width=80, height=60, on_click=number_click, data="0"),
            ft.ElevatedButton("⌫", width=80, height=60, on_click=clear_pin),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        def check_pin(e):
            entered_pin = pin_text.value
            print(f"'{entered_pin}' = '{current_pin}'", flush=True)
            sys.stdout.flush()
            
            # YOUR EXACT DIALOG
            dialog = ft.AlertDialog(
                title=ft.Text("PIN Entered"),
                content=ft.Text(f"You entered: {entered_pin}"),
                
            )
            page.dialog = dialog
            page.show_dialog(dialog)
            
            if entered_pin == current_pin:
                print(f"SUCCESS! '{entered_pin}' matched", flush=True)
                sys.stdout.flush()
                
                show_success_view()
            else:
                print(f"FAILED! '{entered_pin}' != '{current_pin}'", flush=True)
                sys.stdout.flush()
                pin_text.error_text = "Invalid PIN"
                pin_text.update()
        
        check_button = ft.ElevatedButton(
            "✓ Check PIN", 
            on_click=check_pin, 
            width=250, 
            height=50, 
            bgcolor=ft.Colors.GREEN_400, 
            color=ft.Colors.WHITE
        )
        
        main_column = ft.Column([
            pin_text,
            ft.Container(height=20),
            keypad_row1,
            keypad_row2,
            keypad_row3,
            keypad_row4,
            ft.Container(height=20),
            check_button,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)
        
        centered_content = ft.Container(
            content=main_column,
            
            expand=True
        )
        
        page.add(centered_content)
        page.update()

    def show_success_view():
        page.controls.clear()
        
        success_text = ft.Text(
            "You logged in successfully!", 
            size=28, 
            text_align=ft.TextAlign.CENTER, 
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700
        )
        
        logout_button = ft.ElevatedButton(
            "Logout", 
            on_click=lambda e: handle_logout(),
            width=250,
            height=60,
            bgcolor=ft.Colors.RED_400,
            color=ft.Colors.WHITE
        )
        
        success_column = ft.Column([
            success_text,
            ft.Container(height=40),
            logout_button,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        
        centered_content = ft.Container(
            content=success_column,
            
            expand=True
        )
        
        page.add(centered_content)
        page.update()

    def handle_logout():
        nonlocal current_pin
        print("LOGOUT - Generating NEW PIN...", flush=True)
        sys.stdout.flush()
        
        current_pin = generate_new_pin()
        print(f"NEW CURRENT PIN: {current_pin}", flush=True)
        
        sys.stdout.flush()
        
        show_login_view()

    show_login_view()

ft.app(target=main)