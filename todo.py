from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

## Создаем db(database) файл
engine = create_engine("sqlite:///todo.db?check_same_thread=False")

## Создаем объект класса DeclarativeMeta для создания таблицы с характеристиками
## котору мы объявили в классе ниже
Base = declarative_base()


## Описываем таблицу со всеми ее столбцами
class Table(Base):
    __tablename__ = "task"
    id = Column("id", Integer, primary_key=True)
    task_field = Column("task", String, default="You have no tasks to complete!")
    deadline_field = Column("deadline", Date, default=datetime.today())

    def __repr__(self):
        return self.task_field

## Помещаем таблицу в уже созданную базу данных (файл.db)
Base.metadata.create_all(engine)

## Создаем сессию чтобы получить доступ к созданной базе данных с таблицей
## Чтобы взаимодействовать с ней нам нужен только объект session
Session = sessionmaker(bind=engine)
session = Session()

def print_out_tasks():
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    rows = session.query(Table).all()
    count = 1
    print("Все задачи:")
    today = datetime.today()
    if len(rows) == 0:
        print("На сегодня задач нет!")
        return
    for i in range(len(rows)):
        today += timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline_field == today.date()).all()
        for row in rows:
            print(f"{count}. {row.task_field}. {today.day} {today.strftime('%b')}")
            count += 1
    return

def print_out_week_tasks():
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    count = 1
    today = datetime.today()
    for i in range(7):
        today_clone = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline_field == today_clone.date()).all()
        print(f"{week_days[today_clone.weekday()]} {today_clone.day} {today_clone.strftime('%b')}:")
        if len(rows) == 0:
            print("На сегодня задач нет!")
        for row in rows:
            print(f"{count}. {row.task_field}")
            count += 1
        count = 1
    return


def print_out_today_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline_field == today.date()).all()
    print(f"Сегодня {today.day} {today.strftime('%b')}:")
    if len(rows) == 0:
        print("На сегодня задач нет!\n")
        return
    count = 1
    for row in rows:
        print(f"{count}. {row.task_field}")
        count += 1
    print("\n")
    return


def add_tasks():
    #rows = session.query(Table).all()
    task_text = input("Введите задачу:\n")
    deadline_info = input("Введите крайный срок выполения:\n")
    new_row = Table(task_field=task_text, deadline_field=datetime(*[int(i) for i in deadline_info.split("-")]))
    session.add(new_row)
    session.commit()
    print("Задача добавлена!\n")
    return

def print_missed_tasks():
    today = datetime.today()
    missed_task_rows = session.query(Table).filter(Table.deadline_field < today).order_by(Table.deadline_field).all()
    count = 1
    print("Просроченные задачи:")
    if len(missed_task_rows) == 0:
        print("У вас нет просроченных задач!\n")
        return
    for row in missed_task_rows:
        print(f"{count}. {row.task_field}. {row.deadline_field.day} {row.deadline_field.strftime('%b')}")
        count += 1
    print("\n")
    return

def delete_tasks():
    all_rows = session.query(Table).order_by(Table.deadline_field).all()
    count = 1
    if len(all_rows) == 0:
        print("Нечего удалять\n")
        return
    print("Выберите номер задачи, которую хотите удалить:")
    for row in all_rows:
        print(f"{count}. {row.task_field}. {row.deadline_field.day} {row.deadline_field.strftime('%b')}")
        count += 1
    which_to_delete = int(input())
    session.delete(all_rows[which_to_delete - 1])
    session.commit()
    print("Задача удалена!\n")
    return


def main():
    while True:
        print("""1) Задачи на сегодня
2) Задачи на неделю
3) Все задачи
4) Просроченные задачи
5) Добавить задачу
6) Удалить задачу
0) Выйти""")
        command = int(input())
        if command == 0:
            print("Пока!")
            break
        elif command == 1:
            print_out_today_tasks()
        elif command == 2:
            print_out_week_tasks()
        elif command == 3:
            print_out_tasks()
        elif command == 5:
            add_tasks()
        elif command == 4:
            print_missed_tasks()
        elif command == 6:
            delete_tasks()
    return

main()
