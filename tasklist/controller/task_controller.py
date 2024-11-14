# controller/task_controller.py

from model.task_model import TaskModel
from datetime import datetime

class TaskController:
    """Classe para gerenciar a lógica das tarefas, comunicando-se entre a interface e o banco de dados."""

    def __init__(self):
        """Inicializa o controlador com uma instância do modelo."""
        self.model = TaskModel()

    def add_task(self, description, start_date=None, end_date=None):
        """Adiciona uma nova tarefa ao banco de dados, validando os dados.

        Args:
            description (str): Descrição da tarefa.
            start_date (str, opcional): Data de início da tarefa.
            end_date (str, opcional): Data de conclusão da tarefa.

        Returns:
            dict: Resultado com sucesso ou mensagem de erro.
        """
        # Valida descrição obrigatória
        if not description:
            return {"success": False, "message": "A descrição é obrigatória."}

        # Validações de data
        if start_date and end_date:
            if start_date >= end_date:
                return {"success": False, "message": "A data de conclusão deve ser posterior à data de início."}

        # Define o status com base nas datas
        status = self.calculate_status(start_date, end_date)
        
        # Chama o modelo para adicionar a tarefa
        self.model.add_task(description, start_date, end_date, status)
        return {"success": True, "message": "Tarefa adicionada com sucesso."}

    def calculate_status(self, start_date, end_date):
        """Define o status da tarefa com base nas datas fornecidas.

        Args:
            start_date (str): Data de início da tarefa.
            end_date (str): Data de conclusão da tarefa.

        Returns:
            str: Status da tarefa ("Pendente", "Em Andamento" ou "Concluída").
        """
        if not start_date:
            return "Pendente"
        elif start_date and not end_date:
            return "Em Andamento"
        elif start_date and end_date:
            return "Concluída"

    def get_all_tasks(self):
        """Recupera todas as tarefas do banco de dados.

        Returns:
            list: Lista de dicionários com os dados das tarefas.
        """
        return self.model.get_tasks()

    def update_task(self, task_id, description, start_date=None, end_date=None):
        """Atualiza uma tarefa no banco de dados após validação.

        Args:
            task_id (int): ID da tarefa a ser atualizada.
            description (str): Nova descrição da tarefa.
            start_date (str, opcional): Nova data de início.
            end_date (str, opcional): Nova data de conclusão.

        Returns:
            dict: Resultado com sucesso ou mensagem de erro.
        """
        if not description:
            return {"success": False, "message": "A descrição é obrigatória."}

        if start_date and end_date and start_date >= end_date:
            return {"success": False, "message": "A data de conclusão deve ser posterior à data de início."}

        status = self.calculate_status(start_date, end_date)
        self.model.update_task(task_id, description, start_date, end_date, status)
        return {"success": True, "message": "Tarefa atualizada com sucesso."}

    def delete_task(self, task_id):
        """Exclui uma tarefa do banco de dados.

        Args:
            task_id (int): ID da tarefa a ser excluída.

        Returns:
            dict: Resultado da exclusão.
        """
        self.model.delete_task(task_id)
        return {"success": True, "message": "Tarefa excluída com sucesso."}
