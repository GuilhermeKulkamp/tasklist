import flet as ft

class Task(ft.Column):
    """
    Representa uma tarefa na lista de To-Do.

    Args:
        task_name (str): O nome da tarefa.
        task_status_change (callable): Função de callback para alterar o status da tarefa.
        task_delete (callable): Função de callback para deletar a tarefa.
    """
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False  # Indica se a tarefa foi concluída.
        self.task_name = task_name  # Nome da tarefa.
        self.task_status_change = task_status_change  # Callback para mudanças de status.
        self.task_delete = task_delete  # Callback para deletar a tarefa.

        # Checkbox para exibir a tarefa com seu status.
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )

        # Campo de texto para edição do nome da tarefa.
        self.edit_name = ft.TextField(expand=1)

        # Visualização principal da tarefa.
        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        # Botão para editar a tarefa.
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        # Botão para deletar a tarefa.
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        # Visualização de edição da tarefa.
        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                # Botão para salvar as alterações.
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        # Define os controles principais da tarefa.
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        """Callback para ativar o modo de edição da tarefa."""
        self.edit_name.value = self.display_task.label  # Preenche o campo de texto com o nome atual.
        self.display_view.visible = False  # Oculta a visualização principal.
        self.edit_view.visible = True  # Exibe a visualização de edição.
        self.update()  # Atualiza a interface.

    def save_clicked(self, e):
        """Callback para salvar o nome editado da tarefa."""
        self.display_task.label = self.edit_name.value  # Atualiza o nome da tarefa.
        self.display_view.visible = True  # Exibe a visualização principal.
        self.edit_view.visible = False  # Oculta a visualização de edição.
        self.update()  # Atualiza a interface.

    def status_changed(self, e):
        """Callback para alterar o status da tarefa."""
        self.completed = self.display_task.value  # Atualiza o estado de conclusão.
        self.task_status_change(self)  # Chama o callback para notificar a mudança.

    def delete_clicked(self, e):
        """Callback para deletar a tarefa."""
        self.task_delete(self)  # Chama o callback para deletar a tarefa.

class TodoApp(ft.Column):
    """
    Gerencia a aplicação de lista de tarefas (To-Do).

    Args:
        Nenhum argumento é necessário.
    """
    def __init__(self):
        super().__init__()
        # Campo de texto para adicionar novas tarefas.
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True
        )
        # Contêiner para exibir as tarefas.
        self.tasks = ft.Column()

        # Filtro de tarefas (todas, ativas ou concluídas).
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        # Texto indicando a quantidade de tarefas restantes.
        self.items_left = ft.Text("0 items left")

        # Configuração da interface principal.
        self.controls = [
            ft.Row(
                [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]

    def add_clicked(self, e):
        """Adiciona uma nova tarefa à lista."""
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)  # Adiciona a nova tarefa.
            self.new_task.value = ""  # Limpa o campo de texto.
            self.new_task.focus()  # Mantém o foco no campo de texto.
            self.update()  # Atualiza a interface.

    def task_status_change(self, task):
        """Atualiza a interface ao mudar o status de uma tarefa."""
        self.update()

    def task_delete(self, task):
        """Remove uma tarefa da lista."""
        self.tasks.controls.remove(task)  # Remove a tarefa.
        self.update()  # Atualiza a interface.

    def tabs_changed(self, e):
        """Atualiza a lista ao mudar o filtro de visualização."""
        self.update()

    def clear_clicked(self, e):
        """Remove todas as tarefas concluídas."""
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def before_update(self):
        """Atualiza o status das tarefas visíveis e a contagem de itens restantes."""
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and not task.completed)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"

def main(page: ft.Page):
    """
    Configura a aplicação e inicia a interface.
    
    Args:
        page (ft.Page): Página principal da aplicação.
    """
    page.title = "ToDo App"  # Título da aplicação.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Alinhamento horizontal.
    page.scroll = ft.ScrollMode.ADAPTIVE  # Configuração do scroll.

    # Cria a aplicação e adiciona à página.
    page.add(TodoApp())

ft.app(main)
