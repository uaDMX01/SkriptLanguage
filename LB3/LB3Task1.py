#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Програма для роботи з файлами студентів.
Реалізовано читання, запис, дозапис, пошук файлів та даних, сортування за середнім балом.
"""

import os
import re
from typing import List, Dict, Tuple


class StudentManager:
    """
    Клас для управління даними студентів у файлах.
    Кожен файл представляє окрему групу студентів.
    """
    
    def __init__(self, directory_path: str):
        """
        Ініціалізація менеджера студентів.
        
        Args:
            directory_path: Шлях до директорії з файлами груп
        """
        self.directory_path = directory_path
    
    def read_group_file(self, group_name: str) -> List[Tuple[str, float]]:
        """
        Читає дані з файлу групи.
        
        Args:
            group_name: Назва групи
            
        Returns:
            Список кортежів (ім'я студента, середній бал)
        """
        file_path = os.path.join(self.directory_path, f"{group_name}.txt")
        students = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) == 2:
                            name = parts[0]
                            try:
                                avg_grade = float(parts[1])
                                students.append((name, avg_grade))
                            except ValueError:
                                print(f"Помилка при конвертації оцінки для студента {name}. Пропускаємо запис.")
        except FileNotFoundError:
            print(f"Файл для групи {group_name} не знайдено.")
        
        return students
    
    def write_to_group_file(self, group_name: str, students_data: List[Tuple[str, float]]) -> bool:
        """
        Записує дані студентів у файл групи (перезаписуючи існуючий файл).
        
        Args:
            group_name: Назва групи
            students_data: Список кортежів (ім'я студента, середній бал)
            
        Returns:
            True, якщо запис успішний, False - інакше
        """
        file_path = os.path.join(self.directory_path, f"{group_name}.txt")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                for name, avg_grade in students_data:
                    file.write(f"{name}:{avg_grade}\n")
            return True
        except Exception as e:
            print(f"Помилка при записі у файл групи {group_name}: {e}")
            return False
            
    def append_to_group_file(self, group_name: str, students_data: List[Tuple[str, float]]) -> bool:
        """
        Дозаписує дані студентів у файл групи.
        
        Args:
            group_name: Назва групи
            students_data: Список кортежів (ім'я студента, середній бал)
            
        Returns:
            True, якщо дозапис успішний, False - інакше
        """
        file_path = os.path.join(self.directory_path, f"{group_name}.txt")
        
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                for name, avg_grade in students_data:
                    file.write(f"{name}:{avg_grade}\n")
            return True
        except Exception as e:
            print(f"Помилка при дозаписі у файл групи {group_name}: {e}")
            return False
    
    def find_group_files(self) -> List[str]:
        """
        Знаходить всі файли груп у каталозі.
        
        Returns:
            Список назв файлів груп (без розширення)
        """
        group_files = []
        
        try:
            for file_name in os.listdir(self.directory_path):
                if file_name.endswith('.txt'):
                    group_files.append(file_name[:-4])  # Видаляємо розширення .txt
        except Exception as e:
            print(f"Помилка при пошуку файлів груп: {e}")
        
        return group_files
    
    def search_student_in_group(self, group_name: str, student_name: str) -> List[Tuple[str, float]]:
        """
        Шукає студента у файлі групи.
        
        Args:
            group_name: Назва групи
            student_name: Ім'я студента для пошуку (може бути частиною імені)
            
        Returns:
            Список кортежів (ім'я студента, середній бал) для знайдених студентів
        """
        students = self.read_group_file(group_name)
        found_students = []
        
        pattern = re.compile(student_name, re.IGNORECASE)
        for name, avg_grade in students:
            if pattern.search(name):
                found_students.append((name, avg_grade))
        
        return found_students
    
    def search_student_in_all_groups(self, student_name: str) -> Dict[str, List[Tuple[str, float]]]:
        """
        Шукає студента у всіх групах.
        
        Args:
            student_name: Ім'я студента для пошуку (може бути частиною імені)
            
        Returns:
            Словник {назва_групи: [(ім'я_студента, середній_бал), ...]}
        """
        results = {}
        
        for group_name in self.find_group_files():
            found_students = self.search_student_in_group(group_name, student_name)
            if found_students:
                results[group_name] = found_students
        
        return results
    
    def sort_group_by_average_grade(self, group_name: str, ascending: bool = True) -> List[Tuple[str, float]]:
        """
        Сортує дані у файлі групи за середнім балом.
        
        Args:
            group_name: Назва групи
            ascending: True для сортування за зростанням, False - за спаданням
            
        Returns:
            Відсортований список кортежів (ім'я студента, середній бал)
        """
        students = self.read_group_file(group_name)
        sorted_students = sorted(students, key=lambda x: x[1], reverse=not ascending)
        
        # Перезаписуємо файл з відсортованими даними
        file_path = os.path.join(self.directory_path, f"{group_name}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            for name, avg_grade in sorted_students:
                file.write(f"{name}:{avg_grade}\n")
        
        return sorted_students
        



def main():
    """
    Демонстрація роботи програми з файлами студентів.
    """
    # Шлях до директорії з файлами груп
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students_data')
    
    # Створюємо екземпляр менеджера студентів
    manager = StudentManager(directory_path)
    
    # 1. Читання файлів
    print("\n1. Читання даних з файлів груп:")
    for group_name in manager.find_group_files():
        students = manager.read_group_file(group_name)
        print(f"\nГрупа {group_name}:")
        for name, avg_grade in students:
            print(f"  {name}: {avg_grade}")
    
    # 2. Запис у файл
    print("\n2. Запис нових даних у файл Групи_А:")
    new_data = [
        ('Шевченко Олександр', 4.6),
        ('Коваленко Наталія', 4.8),
        ('Бойко Василь', 4.3)
    ]
    if manager.write_to_group_file('Група_А', new_data):
        print("Дані успішно записано у файл Групи_А")
    
    # Перевірка запису
    print("\nДані Групи_А після запису:")
    students = manager.read_group_file('Група_А')
    for name, avg_grade in students:
        print(f"  {name}: {avg_grade}")
    
    # 3. Дозапис у файл
    print("\n3. Дозапис нових студентів до Групи_А:")
    additional_students = [('Мельник Оксана', 4.7), ('Бондаренко Олег', 4.0)]
    if manager.append_to_group_file('Група_А', additional_students):
        print("Студентів успішно додано.")
    
    # Перевірка дозапису
    print("\nДані Групи_А після дозапису:")
    students = manager.read_group_file('Група_А')
    for name, avg_grade in students:
        print(f"  {name}: {avg_grade}")
    
    # 4. Пошук файлів у каталозі
    print("\n4. Пошук файлів у каталозі:")
    group_files = manager.find_group_files()
    for group_name in group_files:
        file_path = os.path.join(directory_path, f"{group_name}.txt")
        file_size = os.path.getsize(file_path)
        print(f"- {group_name}.txt - {file_size} байтів")
    
    # 5. Пошук даних у файлі
    print("\n5. Пошук студентів з іменем 'Василь':")
    results = manager.search_student_in_all_groups('Василь')
    if results:
        for group_name, found_students in results.items():
            print(f"Група {group_name}:")
            for name, avg_grade in found_students:
                print(f"  {name}: {avg_grade}")
    else:
        print("Студентів з іменем 'Василь' не знайдено.")
    
    # 6. Сортування даних у файлі за середнім балом
    print("\n6. Сортування Групи_А за середнім балом (за спаданням):")
    sorted_students = manager.sort_group_by_average_grade('Група_А', ascending=False)
    for name, avg_grade in sorted_students:
        print(f"  {name}: {avg_grade}")
    
    print("\nДемонстрація завершена.")


if __name__ == "__main__":
    main()
