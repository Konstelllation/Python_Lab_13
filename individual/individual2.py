#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
from dotenv import load_dotenv
import os.path
import sys


def add_student(students, name, group, grade):
    students.append(
        {
            'name': name,
            'group': group,
            'grade': grade,
        }
    )
    return students


def display_students(students):
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if students:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('progress', 0)
                )
            )
        print(line)
    else:
        print("Список студентов пуст.")


def select_students(undergraduates):
    """
    Выбрать cтудентов с заданной оценкой.
    """
    # Сформировать список студентов.
    result = []
    # Просмотреть оценки студента
    for pupil in undergraduates:
        # Делаем список оценок
        evaluations = pupil.get('progress')
        list_of_rating = list(evaluations)
        # Ищем нужную оценку
        for i in list_of_rating:
            if i == '2':
                result.append(pupil)
    # Возвратить список выбранных студентов.
    return result

def save_students(file_name, undergraduates):
    """
    Сохранить всех студентов в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установить ensure_ascii=False
        json.dump(undergraduates, fout, ensure_ascii=False, indent=4)
    print("Данные сохранены")


def load_students(file_name):
    """Загрузить всех студентов из файла JSON."""
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        loaded = json.load(fin)
    return loaded



def main(command_line=None):

    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The student's name"
    )
    add.add_argument(
        "-g",
        "--group",
        type=int,
        action="store",
        help="The student's group"
    )
    add.add_argument(
        "-gr",
        "--grade",
        action="store",
        required=True,
        help="The student's grade"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the students"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить имя файла
    data_file = args.data
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    if not data_file:
        data_file = os.getenv("STUDENTS_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        students = load_students(data_file)
    else:
        students = []

    # Добавить студента.
    if args.command == "add":
        students = add_student(
            students,
            args.name,
            args.group,
            args.grade
        )
        is_dirty = True

    # Отобразить всех студентов.
    elif args.command == "display":
        display_students(students)
    # Выбрать требуемых студентов.
    elif args.command == "select":
        selected = select_students(students)
        display_students(selected)

    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(data_file, students)


if __name__ == '__main__':
    main()