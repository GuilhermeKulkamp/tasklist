# main.py

import flet as ft
from view.task_view import TaskApp

def main(page: ft.Page):
    """Função principal que inicializa a interface do aplicativo.

    Args:
        page (ft.Page): Página principal fornecida pela biblioteca Flet.
    """
    # Instancia a aplicação de tarefas
    app = TaskApp()
    # Configura e exibe a interface principal
    app.main(page)

# Ponto de entrada do aplicativo
if __name__ == "__main__":
    # Inicia a aplicação com a função main
    ft.app(target=main)
