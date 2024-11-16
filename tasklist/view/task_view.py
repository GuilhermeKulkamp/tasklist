# view/main_view.py

import flet as ft
from controller.task_controller import TaskController
from datetime import datetime

class TaskApp:
    """Classe principal para a interface do aplicativo de lista de tarefas."""

    def __init__(self):
        """Inicializa o controlador de tarefas e configura o layout."""
        self.controller = TaskController()
        self.tasks = []

    def main(self, page: ft.Page):
        """Configura e exibe a interface do aplicativo.

        Args:
            page (ft.Page): Página principal da interface Flet.
        """
        page.title = "Aplicativo de Lista de Tarefas"
        page.scroll = "auto"

        # Campos do formulário de tarefas
        self.description_field = ft.TextField(label="Descrição", width=300)
        self.start_date_field = ft.TextField(label="Data de Início (AAAA-MM-DD)", width=300)
        self.end_date_field = ft.TextField(label="Data de Conclusão (AAAA-MM-DD)", width=300)
        
        # Botão de adição/atualização
        self.submit_button = ft.ElevatedButton(text="Adicionar Tarefa", on_click=self.add_task)

        # Contêiner para exibir tarefas
        self.tasks_list = ft.Column()

        # Adicionando componentes à página
        page.add(
            ft.Column([
                self.description_field,
                self.start_date_field,
                self.end_date_field,
                self.submit_button,
                self.tasks_list
            ])
        )

        # Carregar tarefas existentes
        self.load_tasks()

    def load_tasks(self):
        """Carrega todas as tarefas do banco de dados e atualiza a lista na interface."""
        self.tasks = self.controller.get_all_tasks()
        self.tasks_list.controls.clear()
        for task in self.tasks:
            self.tasks_list.controls.append(self.create_task_row(task))

    def create_task_row(self, task):
        """Cria uma linha visual para uma tarefa.

        Args:
            task (dict): Dicionário com dados da tarefa.

        Returns:
            ft.Row: Linha contendo a tarefa e seus botões de controle.
        """
        return ft.Row(
            controls=[
                ft.Text(f"ID: {task['id']}"),
                ft.Text(task["description"]),
                ft.Text(f"Início: {task['start_date'] or 'N/A'}"),
                ft.Text(f"Conclusão: {task['end_date'] or 'N/A'}"),
                ft.Text(f"Status: {task['status']}"),
                ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: self.edit_task(task)),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: self.delete_task(task['id']))
            ]
        )

    def add_task(self, event):
        """Adiciona uma nova tarefa com os dados do formulário.

        Args:
            event (ft.ControlEvent): Evento de clique do botão de adicionar.
        """
        description = self.description_field.value
        start_date = self.start_date_field.value
        end_date = self.end_date_field.value

        # Chama o controlador para adicionar a tarefa
        result = self.controller.add_task(description, start_date, end_date)

        # Exibe mensagem de feedback
        if result["success"]:
            self.load_tasks()  # Recarrega a lista de tarefas
            self.clear_form()
        else:
            print(result["message"])

    def edit_task(self, task):
        """Preenche o formulário com os dados de uma tarefa para edição.

        Args:
            task (dict): Dados da tarefa a ser editada.
        """
        self.description_field.value = task["description"]
        self.start_date_field.value = task["start_date"] or ""
        self.end_date_field.value = task["end_date"] or ""
        self.submit_button.text = "Atualizar Tarefa"
        self.submit_button.on_click = lambda e: self.update_task(task["id"])

    def update_task(self, task_id):
        """Atualiza uma tarefa existente com os dados do formulário.

        Args:
            task_id (int): ID da tarefa a ser atualizada.
        """
        description = self.description_field.value
        start_date = self.start_date_field.value
        end_date = self.end_date_field.value

        # Chama o controlador para atualizar a tarefa
        result = self.controller.update_task(task_id, description, start_date, end_date)

        # Exibe mensagem de feedback
        if result["success"]:
            self.load_tasks()
            self.clear_form()
        else:
            print(result["message"])

    def delete_task(self, task_id):
        """Exclui uma tarefa com base no ID fornecido.

        Args:
            task_id (int): ID da tarefa a ser excluída.
        """
        result = self.controller.delete_task(task_id)
        print(result["message"])  # Exibe a mensagem de sucesso
        self.load_tasks()  # Recarrega a lista de tarefas

    def clear_form(self):
        """Limpa o formulário de tarefas."""
        self.description_field.value = ""
        self.start_date_field.value = ""
        self.end_date_field.value = ""
        self.submit_button.text = "Adicionar Tarefa"
        self.submit_button.on_click = self.add_task

# Inicializando a aplicação
#def main(page: ft.Page):
#    app = TaskApp()
#    app.main(page)
#
#ft.app(target=main)
