# model/task_model.py

import sqlite3
from datetime import datetime

class TaskModel:
    """Classe para gerenciamento do banco de dados das tarefas."""

    def __init__(self, db_path="db/database.db"):
        """Inicializa a conexão com o banco de dados e cria a tabela se não existir.

        Args:
            db_path (str): Caminho do arquivo do banco de dados.
        """
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        """Estabelece uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Conexão com o banco de dados.
        """
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        """Cria a tabela 'tasks' no banco de dados, se ainda não existir."""
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT,
                status TEXT
            )
        ''')
        connection.commit()
        connection.close()

    def add_task(self, description, start_date=None, end_date=None, status="Pendente"):
        """Adiciona uma nova tarefa ao banco de dados.

        Args:
            description (str): Descrição da tarefa.
            start_date (str, opcional): Data de início da tarefa.
            end_date (str, opcional): Data de conclusão da tarefa.
            status (str): Status da tarefa.
        """
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO tasks (description, start_date, end_date, status)
            VALUES (?, ?, ?, ?)
        ''', (description, start_date, end_date, status))
        connection.commit()
        connection.close()

    def get_tasks(self):
        """Recupera todas as tarefas do banco de dados.

        Returns:
            list: Lista de dicionários com as informações das tarefas.
        """
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        connection.close()
        tasks = []
        for row in rows:
            tasks.append({
                "id": row[0],
                "description": row[1],
                "start_date": row[2],
                "end_date": row[3],
                "status": row[4]
            })
        return tasks

    def update_task(self, task_id, description, start_date=None, end_date=None, status="Pendente"):
        """Atualiza uma tarefa no banco de dados.

        Args:
            task_id (int): ID da tarefa a ser atualizada.
            description (str): Nova descrição da tarefa.
            start_date (str, opcional): Nova data de início.
            end_date (str, opcional): Nova data de conclusão.
            status (str): Novo status da tarefa.
        """
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE tasks
            SET description = ?, start_date = ?, end_date = ?, status = ?
            WHERE id = ?
        ''', (description, start_date, end_date, status, task_id))
        connection.commit()
        connection.close()

    def delete_task(self, task_id):
        """Exclui uma tarefa do banco de dados.

        Args:
            task_id (int): ID da tarefa a ser excluída.
        """
        connection = self._connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()
