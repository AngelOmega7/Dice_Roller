import flet as ft
import sqlite3
from uuid import uuid4
from dice import roll_die
from notes import load_notes, save_note, delete_note

def main(page: ft.Page):
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.title = "Dice Roller"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    result_text = ft.Text(
        value="Roll a die!", size=30, weight=ft.FontWeight.BOLD,
        color="#F1F5F9",
    )

    # Shared colors for all dice buttons; hex values can be customized here.
    button_style = ft.ButtonStyle(
        color="#102A2E",
        bgcolor={
            ft.ControlState.HOVERED: "#99F6E4",
            ft.ControlState.DEFAULT: "#5EEAD4",
        },
    )

    def roll(sides: int):
        result_text.value = f"D{sides} Result: {roll_die(sides)}"
        page.update()

    roller_page = ft.SafeArea(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    result_text,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Button(
                                ft.Text("Roll d20", size=24, weight=ft.FontWeight.BOLD),
                                width=200,
                                height=64,
                                style=button_style,
                                on_click=lambda e: roll(20),
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Button("Roll d4", style=button_style, on_click=lambda e: roll(4)),
                            ft.Button("Roll d6", style=button_style, on_click=lambda e: roll(6)),
                            ft.Button("Roll d8", style=button_style, on_click=lambda e: roll(8)),
                            ft.Button("Roll d10", style=button_style, on_click=lambda e: roll(10)),
                            ft.Button("Roll d12", style=button_style, on_click=lambda e: roll(12)),
                            ft.Button("Roll d100", style=button_style, on_click=lambda e: roll(100)),
                        ]
                    )
                ]
            )
    )

    notes_field = ft.TextField(
        value="",
        label="Notes",
        hint_text="Write your notes here…",
        multiline=True,
        expand=True,
        min_lines=15,
        color="#F1F5F9",
        bgcolor="#1E293B",
        border_color="#64748B",
        focused_border_color="#5EEAD4",
        text_size=18,
    )
    notes_status = ft.Text(color="#CBD5E1")
    storage_available = True
    try:
        saved_notes = load_notes()
    except sqlite3.Error as error:
        saved_notes = {}
        storage_available = False
        notes_status.value = f"Could not load notes: {error}"

    current_note_id = None
    note_title = ft.TextField(
        label="Note title", color="#F1F5F9", bgcolor="#1E293B",
        focused_border_color="#5EEAD4",
    )
    note_selector = ft.Dropdown(
        label="Saved notes", color="#F1F5F9", bgcolor="#1E293B",
        expand=True,
    )

    def refresh_note_selector():
        note_selector.options = [
            ft.DropdownOption(key=note_id, text=note["title"])
            for note_id, note in saved_notes.items()
        ]
        note_selector.value = current_note_id

    def open_note(note_id):
        nonlocal current_note_id
        current_note_id = note_id
        note = saved_notes.get(note_id, {"title": "", "body": ""})
        note_title.value = note["title"]
        notes_field.value = note["body"]
        refresh_note_selector()

    def save_current_note(e=None):
        nonlocal current_note_id
        note_id = current_note_id or str(uuid4())
        title = (note_title.value or "").strip() or "Untitled note"
        body = notes_field.value or ""
        try:
            save_note(note_id, title, body)
        except sqlite3.Error as error:
            notes_status.value = f"Could not save note: {error}"
            page.update()
            return False
        saved_notes[note_id] = {"title": title, "body": body}
        current_note_id = note_id
        note_title.value = title
        refresh_note_selector()
        notes_status.value = "Saved."
        page.update()
        return True

    def save_before_switch():
        # Do not create empty notes merely by navigating.
        if current_note_id or note_title.value or notes_field.value:
            return save_current_note()
        return True

    def new_note(e):
        if save_before_switch():
            open_note(None)
            notes_status.value = "New note — click Save when ready."
            page.update()

    def switch_note(e):
        selected_id = note_selector.value
        if save_before_switch():
            open_note(selected_id)
            notes_status.value = "Note opened."
        else:
            note_selector.value = current_note_id
        page.update()

    def remove_note(e):
        if current_note_id is not None:
            try:
                delete_note(current_note_id)
            except sqlite3.Error as error:
                notes_status.value = f"Could not delete note: {error}"
                page.update()
                return
            del saved_notes[current_note_id]
        open_note(next(iter(saved_notes), None))
        notes_status.value = "Note deleted."
        page.update()

    note_selector.on_select = switch_note
    open_note(next(iter(saved_notes), None))
    notes_page = ft.Container(
        content=ft.Column(
            expand=True,
            controls=[
                ft.Row(controls=[note_selector]),
                ft.Row(
                    wrap=True,
                    controls=[
                        ft.Button("New", style=button_style, on_click=new_note),
                        ft.Button("Save", style=button_style, on_click=save_current_note),
                        ft.Button("Delete", style=button_style, on_click=remove_note),
                    ],
                ),
                note_title,
                notes_field,
                notes_status,
                ft.Text("Notes save when switching notes. Click Save before closing the app.",
                        color="#CBD5E1", size=12),
            ],
            disabled=not storage_available,
        ),
        padding=20,
        expand=True,
        visible=False,
    )

    def show_page(name: str):
        roller_page.visible = name == "dice"
        notes_page.visible = name == "notes"
        page.title = "Notes" if name == "notes" else "Dice Roller"
        page.update()

    page.add(
        ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Button("Dice Roller", style=button_style,
                                  on_click=lambda e: show_page("dice")),
                        ft.Button("Notes", style=button_style,
                                  on_click=lambda e: show_page("notes")),
                    ],
                ),
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[roller_page, notes_page],
                ),
            ],
        )
    )

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
