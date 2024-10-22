import flet as ft
import os

# Función principal
def main(page: ft.Page):
    configurar_pagina(page)
    shopping_list = []  # Lista de compras

    # Crear la cabecera con logo y texto de bienvenida
    header = crear_cabecera()

    # Campo de texto para añadir ítems
    new_task = ft.TextField(hint_text="¿Qué necesitas comprar?", width=250)
    
    # Fila para los botones
    button_row = ft.Row(
        [new_task, ft.ElevatedButton("Agregar", on_click=lambda e: add_clicked(e, new_task, shopping_list, page))],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Añadir elementos a la página, todo centrado
    page.add(
        ft.Column(
            [
                header,
                ft.Divider(height=20),  # Separador entre el logo y el campo de texto
                button_row,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    
    # Actualizar botones si hay ítems
    update_buttons(page, shopping_list)

# Función para configurar la página
def configurar_pagina(page):
    page.title = "Lista de Compras"
    page.bgcolor = "#2c3e50" 
    page.window.width = 600
    page.window.height = 400

# Función para crear la cabecera con el logo y el texto de bienvenida
def crear_cabecera():
    logo_path = os.path.join(os.path.dirname(__file__), "./logo.png")
    logo = ft.Image(src=logo_path, width=200, height=150)
    header_text = ft.Text("Bienvenidos a la App de Lista de Compras", size=20, weight=ft.FontWeight.BOLD, color="#ecf0f1")  # Color texto gris claro

    header = ft.Column(
        [logo, header_text],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    return header

# Función para manejar el clic de agregar ítems
def add_clicked(e, new_task, shopping_list, page):
    item = create_item(new_task.value, shopping_list, page)
    shopping_list.append(new_task.value)
    page.add(item)
    new_task.value = ""
    new_task.focus()

    # Actualizar los botones
    update_buttons(page, shopping_list)

# Función para crear un ítem con checkbox y botones de edición/eliminación
def create_item(text, shopping_list, page):
    checkbox = ft.Checkbox(label=text)
    item = ft.Row(
        [
            checkbox, 
            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item, shopping_list, page)),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, text, shopping_list, page))
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    return item

# Función para editar un ítem
def edit_clicked(e, checkbox, item, shopping_list, page):
    new_value = ft.TextField(value=checkbox.label, width=300)
    item.controls = [
        new_value, 
        ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: save_clicked(e, checkbox, new_value, item, shopping_list, page)),
        ft.IconButton(icon=ft.icons.CANCEL, on_click=lambda e: cancel_clicked(e, checkbox, item, shopping_list, page))
    ]
    page.update()

# Función para guardar cambios en un ítem
def save_clicked(e, checkbox, new_value, item, shopping_list, page):
    old_value = checkbox.label  # Guardar el valor antiguo
    checkbox.label = new_value.value
    if old_value in shopping_list:  # Actualizar la lista si el ítem existe
        shopping_list[shopping_list.index(old_value)] = new_value.value
    item.controls = [
        checkbox, 
        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item, shopping_list, page)),
        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label, shopping_list, page))
    ]
    page.update()

# Función para cancelar la edición
def cancel_clicked(e, checkbox, item, shopping_list, page):
    item.controls = [
        checkbox, 
        ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item, shopping_list, page)),
        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label, shopping_list, page))
    ]
    page.update()

# Función para eliminar un ítem
def delete_clicked(e, item, text, shopping_list, page):
    if text in shopping_list:  # Comprobar si el ítem existe antes de eliminar
        shopping_list.remove(text)
        page.controls.remove(item)
        page.update()
        update_buttons(page, shopping_list)

# Función para actualizar los botones según la lista
def update_buttons(page, shopping_list):
    button_row = page.controls[0].controls[2]  # Obtener la fila de botones
    button_row.controls = [button_row.controls[0], ft.ElevatedButton("Agregar", on_click=lambda e: add_clicked(e, button_row.controls[0], shopping_list, page))]
    page.update()

ft.app(target=main)
