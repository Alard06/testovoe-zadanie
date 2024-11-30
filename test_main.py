import pytest
from main import TaskManagement


@pytest.fixture
def task_manager(tmpdir):
    """Создание временного экземпляра TaskManagement для тестирования."""
    test_file = tmpdir.join("test_tasks.json")
    manager = TaskManagement(data_file=str(test_file))
    return manager


def test_add_task(task_manager):
    """Тестирование добавления задачи."""
    task_manager.add_task("Задача 1", "Описание задачи 1", "Работа", "2024-12-01")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0]["title"] == "Задача 1"


def test_update_task(task_manager):
    """Тестирование обновления задачи."""
    task_manager.add_task("Задача 1", "Описание задачи 1", "Работа", "2024-12-01")
    task_manager.update_task(1, title="Обновленная задача", description="Новое описание")
    assert task_manager.tasks[0]["title"] == "Обновленная задача"
    assert task_manager.tasks[0]["description"] == "Новое описание"


def test_delete_task(task_manager):
    """Тестирование удаления задачи по ID."""
    task_manager.add_task("Задача 1", "Описание задачи 1", "Работа", "2024-12-01")
    task_manager.delete_task(id_task=1)
    assert len(task_manager.tasks) == 0


def test_show_task(task_manager):
    """Тестирование отображения задачи."""
    task_manager.add_task("Задача 1", "Описание задачи 1", "Работа", "2024-12-01")
    task = task_manager.show_task(id_task=1)
    assert task["title"] == "Задача 1"


def test_find_task(task_manager):
    """Тестирование поиска задачи по ID."""
    task_manager.add_task("Задача 1", "Описание задачи 1", "Работа", "2024-12-01")
    task = task_manager.find_task(id_task=1)
    assert task["title"] == "Задача 1"


def test_invalid_date_format(task_manager):
    """Тестирование обработки неверного формата даты при добавлении задачи."""
    task_manager.add_task("Задача 1", "Описание задачи 1", "Работа", "неверная_дата")
    assert len(task_manager.tasks) == 0


def test_update_nonexistent_task(task_manager):
    """Тестирование обновления несуществующей задачи."""
    task_manager.update_task(999, title="Обновленная задача")
    assert len(task_manager.tasks) == 0


def test_delete_nonexistent_task(task_manager):
    """Тестирование удаления несуществующей задачи."""
    task_manager.delete_task(id_task=999)
    assert len(task_manager.tasks) == 0


if __name__ == "__main__":
    pytest.main()
