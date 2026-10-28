import random
import flet as ft

def main(page: ft.Page):
	page.content = "Dice Roller"
	page.vertical_alignment = ft.MainAxisAlignment.CENTER
	page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

	result_text = ft.Text(
		value="Roll a die!", size=30, weight=ft.FontWeight.BOLD
	)
	def roll_die(sides: int):
		roll = random.randint(1, sides)
		result_text.value = f"D{sides} Result: {roll}"
		page.update()

	def roll_d4():
		roll_die(4)
	def roll_d6():
		roll_die(6)
	def roll_d8():
		roll_die(8)
	def roll_d10():
		roll_die(10)
	def roll_d12():
		roll_die(12)
	def roll_d20():
		roll_die(20)
	def roll_d100():
		roll_die(100)
	page.add(
		ft.SafeArea(
			ft.Column(
				horizontal_alignment=ft.CrossAxisAlignment.CENTER,
				spacing=20,
				controls=[
					result_text,
					ft.Row(
						alignment=ft.MainAxisAlignment.CENTER,
						spacing=10,
						controls=[
							ft.Button("Roll d4", on_click=roll_d4),
							ft.Button("Roll d6", on_click=roll_d6),
							ft.Button("Roll d8", on_click=roll_d8),
							ft.Button("Roll d10", on_click=roll_d10),
							ft.Button("Roll d12", on_click=roll_d12),
							ft.Button("Roll d20", on_click=roll_d20),
							ft.Button("Roll d100", on_click=roll_d100),
						]
					)
				]
			)
		)
	)

ft.run(main)

