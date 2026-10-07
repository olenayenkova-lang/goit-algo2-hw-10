"""Завдання 2. Складання розкладу занять жадібним алгоритмом (покриття множини)."""


class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = set(can_teach_subjects)
        self.assigned_subjects = set()

    def __repr__(self):
        return f"Teacher({self.first_name} {self.last_name}, {self.age})"


def create_schedule(subjects, teachers):
    """Жадібний алгоритм покриття множини.

    На кожному кроці обирається викладач, який покриває найбільше ще не
    охоплених предметів; при рівності — наймолодший. Якщо покрити всі
    предмети неможливо, повертається None.
    """
    uncovered = set(subjects)
    available = list(teachers)
    schedule = []

    for t in available:
        t.assigned_subjects = set()

    while uncovered:
        best = None
        best_cover = set()

        for teacher in available:
            cover = teacher.can_teach_subjects & uncovered
            if not cover:
                continue
            if best is None or len(cover) > len(best_cover) or (
                len(cover) == len(best_cover) and teacher.age < best.age
            ):
                best, best_cover = teacher, cover

        if best is None:  # жоден викладач не може покрити решту предметів
            return None

        best.assigned_subjects = best_cover
        schedule.append(best)
        uncovered -= best_cover
        available.remove(best)

    return schedule


if __name__ == "__main__":
    # Множина предметів
    subjects = {"Математика", "Фізика", "Хімія", "Інформатика", "Біологія"}
    # Створення списку викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"}),
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("Розклад занять:")
        for teacher in schedule:
            print(f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, email: {teacher.email}")
            print(f"   Викладає предмети: {', '.join(sorted(teacher.assigned_subjects))}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
