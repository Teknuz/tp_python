import flet as ft

def main(page):
    page.window_width = 600
    page.window_height = 500
    page.title = "Lista de Compras"
    page.theme_mode = "light"  # Inicia en modo claro

    tasks = []

    def update_counters():
        """Actualiza los contadores de productos pendientes y listos."""
        pending = sum(1 for task in tasks if not task["checkbox"].value)
        completed = len(tasks) - pending

        counter_pending.value = f"Productos pendientes: {pending}"
        counter_completed.value = f"Productos listos: {completed}"

        counter_pending.update()
        counter_completed.update()

    def add_clicked(e):
        """Añade un producto a la lista."""
        if product_name.value.strip() and product_quantity.value.strip():
            task_checkbox = ft.Checkbox(
                label=f"{product_name.value} - {product_quantity.value} ",
                value=False,
                on_change=task_status_changed
            )
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE, on_click=lambda e: delete_task(task_checkbox)
            )
            edit_button = ft.IconButton(
                icon=ft.icons.EDIT, on_click=lambda e: edit_task(task_checkbox)
            )

            tasks.append({
                "checkbox": task_checkbox,
                "delete_button": delete_button,
                "edit_button": edit_button
            })

            task_list.controls.append(
                ft.Row([task_checkbox, edit_button, delete_button], alignment="spaceBetween")
            )
            task_list.update()

            product_name.value = ""
            product_quantity.value = ""
            product_name.focus()
            update_counters()

    def delete_task(task_checkbox):
        """Elimina un producto de la lista."""
        for task in tasks:
            if task["checkbox"] == task_checkbox:
                tasks.remove(task)
                task_list.controls.remove(task_checkbox.parent)
                break
        task_list.update()
        update_counters()

    def task_status_changed(e):
        """Actualiza los contadores al marcar o desmarcar un producto."""
        update_counters()

    def edit_task(task_checkbox):
        """Permite editar un producto."""
        task_row = task_checkbox.parent
        name, quantity = task_checkbox.label.split(" - ")

        edit_name = ft.TextField(value=name, width=200)
        edit_quantity = ft.TextField(value=quantity.split()[0], width=100)

        confirm_button = ft.IconButton(
            icon=ft.icons.CHECK,
            on_click=lambda e: confirm_edit(task_checkbox, edit_name, edit_quantity, task_row)
        )

        task_row.controls.clear()
        task_row.controls.append(
            ft.Row([edit_name, edit_quantity, confirm_button], alignment="spaceBetween")
        )
        task_row.update()

    def confirm_edit(task_checkbox, edit_name, edit_quantity, task_row):
        """Confirma la edición de un producto."""
        task_checkbox.label = f"{edit_name.value} - {edit_quantity.value} "
        task_row.controls.clear()
        task_row.controls.extend([
            task_checkbox,
            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_task(task_checkbox)),
            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_task(task_checkbox))
        ])
        task_row.update()

    def toggle_theme(e):
        """Alterna entre modo claro y oscuro."""
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        toggle_theme_button.text = "Modo Claro" if page.theme_mode == "dark" else "Modo Oscuro"
        toggle_theme_button.update()
        page.update()

    # Campos de entrada para nombre y cantidad del producto
    product_name = ft.TextField(hint_text="Producto", width=200)
    product_quantity = ft.TextField(hint_text="Cantidad", width=100)
    add_button = ft.ElevatedButton("Agregar", on_click=add_clicked)

    # Botón para alternar entre modo claro y oscuro
    toggle_theme_button = ft.ElevatedButton("Modo Oscuro", on_click=toggle_theme)

    # Logo e información de la cabecera
    logo = ft.Image(
        src=r"C:\Users\Jose\Downloads\python\python\Jose_Gomez\TP\logo.jpg",
        width=150, height=150
    )
    header_text = ft.Text(
        "Bienvenidos a la App de Lista de Compras", size=20, weight=ft.FontWeight.BOLD
    )

    # Crear la cabecera
    header = ft.Column([logo, header_text], alignment="center")

    # Contenedores para la lista de tareas y los contadores
    task_list = ft.ListView(expand=True, spacing=10, padding=20)

    counter_pending = ft.Text("Productos pendientes: 0", size=16, weight=ft.FontWeight)
    counter_completed = ft.Text("Productos listos: 0", size=16, weight=ft.FontWeight)

    # Añadir elementos a la página
    page.add(
        header,
        ft.Divider(height=20),
        ft.Row([product_name, product_quantity, add_button, toggle_theme_button], alignment="center"),
        ft.Divider(height=10),
        counter_pending,
        counter_completed,
        task_list,
    )

ft.app(main)
