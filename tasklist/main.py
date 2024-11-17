# main.py

import flet as ft
from view.todo_view import TodoApp

'''
def main(page: ft.Page):
    """Função principal que inicializa a interface do aplicativo.

    Args:
        page (ft.Page): Página principal fornecida pela biblioteca Flet.
    """
    # Instancia a aplicação de tarefas
    app = TaskApp()
    # Configura e exibe a interface principal
    app.main(page)
'''


def main(page: ft.Page):
    """
    Configura a aplicação e inicia a interface.
    
    Args:
        page (ft.Page): Página principal da aplicação.
    """
    
    page.title = "ToDo App"  # Título da aplicação.
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Alinhamento horizontal.
    page.scroll = ft.ScrollMode.ADAPTIVE  # Configuração do scroll.

    # instancia a aplicação de tarefas
    #app = TodoApp()

    # Cria a aplicação e adiciona à página.
    page.add(TodoApp())


# Ponto de entrada do aplicativo
if __name__ == "__main__":
    # Inicia a aplicação com a função main
    ft.app(target=main)
