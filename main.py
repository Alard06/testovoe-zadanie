import json
from datetime import datetime


class TaskManagement:
    """
    Класс для управления задачами
    """

    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла"""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        """Сохранение задач в файл"""
        with open(self.data_file, "w") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def generate_id(self):
        """Генерация уникального идентификатора"""
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1

    def add_task(self, title: str, description: str, category: str,
                 date: str, priority: str = 'Низкий', status: str = 'Не выполнена') -> None:
        """Функция для создания записи"""
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Неверный формат даты. Задача не добавлена.")
            return

        task = {
            "id": self.generate_id(),
            "title": title,
            "description": description,
            "category": category,
            "due_date": date,
            "priority": priority.capitalize(),
            "status": status
        }
        self.tasks.append(task)
        self.save_tasks()
        print("Задача успешно добавлена!")

    def update_task(self, id_task: int, title: str = None, description: str = None,
                    category: str = None, date: str = None, priority: str = None, status: str = None) -> None:
        """Функция для обновления записи"""
        task = next((task for task in self.tasks if task["id"] == id_task), None)
        if not task:
            print("Задача с таким ID не найдена.")
            return

        if title:
            task["title"] = title
        if description:
            task["description"] = description
        if category:
            task["category"] = category
        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                task["due_date"] = date
            except ValueError:
                print("Неверный формат даты. Задача не обновлена.")
                return
        if priority:
            task["priority"] = priority.capitalize()
        if status:
            task["status"] = status

        self.save_tasks()
        print("Задача успешно обновлена!")

    def delete_task(self, id_task: int = None, title: str = None) -> None:
        """Функция для удаления записи"""
        if id_task:
            self.tasks = [task for task in self.tasks if task["id"] != id_task]
        elif title:
            self.tasks = [task for task in self.tasks if task["title"].lower() != title.lower()]
        else:
            print("Необходимо указать ID или название задачи для удаления.")
            return

        self.save_tasks()
        print("Задача успешно удалена!")

    def show_task(self, id_task: int = None, title: str = None) -> dict or None:
        """Функция для отображения задачи"""
        if id_task:
            task = next((task for task in self.tasks if task["id"] == id_task), None)
        elif title:
            task = next((task for task in self.tasks if task["title"].lower() == title.lower()), None)
        else:
            print("Необходимо указать ID или название задачи для отображения.")
            return None

        if task:
            print(f"ID: {task['id']}, Название: {task['title']}, Описание: {task['description']}, "
                  f"Категория: {task['category']}, Срок: {task['due_date']}, "
                  f"Приоритет: {task['priority']}, Статус: {task['status']}")
            return task  # Возвращаем задачу
        else:
            print("Задача не найдена.")
            return None

    def find_task(self, id_task: int = None, title: str = None):
        """Функция для поиска задачи"""
        if id_task:
            return next((task for task in self.tasks if task["id"] == id_task), None)
        elif title:
            return next((task for task in self.tasks if task["title"].lower() == title.lower()), None)
        else:
            print("Необходимо указать ID или название задачи для поиска.")
            return None


class TaskManager(TaskManagement):
    """
    Класс для управления приложением
    """

    def __init__(self):
        super().__init__()
        self.run = True

    def start_app(self):
        """Запуск приложения"""
        while self.run:
            print("\nМеню:")
            print("1. Добавить задачу")
            print("2. Обновить задачу")
            print("3. Удалить задачу")
            print("4. Показать задачу")
            print("5. Найти задачу")
            print("6. Показать все задачи")
            print("0. Выход")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                title = input("Введите название задачи: ").strip()
                description = input("Введите описание задачи: ").strip()
                category = input("Введите категорию задачи: ").strip()
                date = input("Введите срок выполнения задачи (YYYY-MM-DD): ").strip()
                priority = input("Введите приоритет задачи (низкий, средний, высокий): ").strip()
                self.add_task(title, description, category, date, priority)
            elif choice == "2":
                id_task = int(input("Введите ID задачи для обновления: "))
                title = input("Введите новое название задачи (или оставьте пустым): ").strip()
                description = input("Введите новое описание задачи (или оставьте пустым): ").strip()
                category = input("Введите новую категорию задачи (или оставьте пустым): ").strip()
                date = input("Введите новый срок выполнения задачи (YYYY-MM-DD, или оставьте пустым): ").strip()
                priority = input("Введите новый приоритет задачи (или оставьте пустым): ").strip()
                status = input("Введите новый статус задачи (или оставьте пустым): ").strip()
                self.update_task(id_task, title, description, category, date, priority, status)
            elif choice == "3":
                id_task = int(input("Введите ID задачи для удаления: "))
                self.delete_task(id_task=id_task)
            elif choice == "4":
                id_task = int(input("Введите ID задачи для отображения: "))
                self.show_task(id_task=id_task)
            elif choice == "5":
                id_task = int(input("Введите ID задачи для поиска: "))
                task = self.find_task(id_task=id_task)
                if task:
                    print(task)
                else:
                    print("Задача не найдена.")
            elif choice == "6":
                for task in self.tasks:
                    print(task)
            elif choice == "0":
                print("Выход из программы.")
                self.run = False
            else:
                print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    manager = TaskManager()
    manager.start_app()
