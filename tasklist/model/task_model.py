# model/task_model.py

import sqlite3
import os

class TaskModel:
    """Modelo para gerenciar operações de banco de dados da lista de tarefas."""

    def __init__(self):
        """Inicializa a conexão com o banco de dados e cria a tabela se necessário."""
        # Caminho do banco de dados
        self.db_path = "taskslist.db"
        # Inicializa o banco de dados
        self.initialize_database()

    def initialize_database(self):
        """Verifica e cria o banco de dados e a tabela de tarefas, se ainda não existirem."""
        # Verifica se o arquivo do banco de dados existe
        if not os.path.exists(self.db_path):
            # Conecta e cria a tabela
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        start_date TEXT,
                        end_date TEXT,
                        status TEXT
                    );
                """)
                conn.commit()
                print("Banco de dados criado com sucesso.")

    def add_task(self, description, start_date=None, end_date=None, status="Pendente"):
        """Adiciona uma nova tarefa ao banco de dados.

        Args:
            description (str): Descrição da tarefa.
            start_date (str, opcional): Data de início da tarefa.
            end_date (str, opcional): Data de conclusão da tarefa.
            status (str): Status da tarefa.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (description, start_date, end_date, status)
                VALUES (?, ?, ?, ?);
            """, (description, start_date, end_date, status))
            conn.commit()

    def get_tasks(self):
        """Obtém todas as tarefas do banco de dados.

        Returns:
            list: Lista de dicionários representando as tarefas.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, description, start_date, end_date, status FROM tasks;")
            rows = cursor.fetchall()
            tasks = [
                {"id": row[0], "description": row[1], "start_date": row[2], "end_date": row[3], "status": row[4]}
                for row in rows
            ]
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
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks
                SET description = ?, start_date = ?, end_date = ?, status = ?
                WHERE id = ?;
            """, (description, start_date, end_date, status, task_id))
            conn.commit()

    def delete_task(self, task_id):
        """Exclui uma tarefa do banco de dados.

        Args:
            task_id (int): ID da tarefa a ser excluída.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
            conn.commit()
