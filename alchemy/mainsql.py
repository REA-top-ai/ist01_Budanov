from database import SessionLocal, engine, Base
from models import Author, Post, Comment
from crud import *

def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        print("Начианем тестирование...\n")
        print("Создаем авторов...")
        author1 = create_author(session, "Ирина", "irina@example.com")
        author2 = create_author(session, "Дмитрий", "dmitriy@example.com")
        print(f"{author1.name} (id={author1.id})")
        print(f"{author2.name} (id={author2.id})\n")

        print("Создаем посты...")
        post1 = create_post(session, "Первый пост", "Это содержание первого поста. Оно достаточно длинное.", author1.id, published = True)
        post2 = create_post(session, "Черновик", "Этот пост пока не опубликован.", author1.id, published = False)
        post3 = create_post(session, "Пост Ивана", "Текст от Ивана.", author2.id, published = True)
        print(f"'{post1.title}' (опубликован)")
        print(f"'{post2.title}' (черновик)")
        print(f"'{post3.title}' (опубликован)\n")

        print("Добавляем комментарии...")
        add_comment(session, post1.id, "Читатель1", "Отличная статьяб оченб полезно!")
        add_comment(session, post1.id, "Читатель2", "Спасибо за материал, жду продолжения.")
        add_comment(session, post1.id, "Аноним", "Коротко.")
        print("3 комментария добвлены к первому посту\n")

        print("Публикуем черновик...")
        success = update_post_status(session, post2.id, published = True)
        if success:
            print(f"'{post2.title}' теперь опублкован\n")

        print("Все опубликованные посты:")
        published = get_published_posts(session)
        for post in published:
            print(f"'{post.title}' - автор {post.author.name}")
        print()

        print("Топ авторов по количеству постов:")
        top_authors = get_top_authors_by_posts(session, limit = 3)
        for rank, (name, count) in enumerate(top_authors, 1):
            print(f"{rank}. {name}: {count} пост(ов)")
        print()

        print("Поиск автоора по email...")
        found = get_author_by_email(session, "anna@example.com")
        if found:
            print(f"Найдено: {found.name}")
        else:
            print("Автор не найден")

        print("\nЗадание 1: Поиск автора по имени")
        author_by_name = get_author_by_name(session, "Анна Петрова")
        if author_by_name:
            print(f"Найден автор: {author_by_name.name} (email: {author_by_name.email})")

        print("\nЗадание 2: Посты за определенную дату")
        from datetime import datetime
        today_str = datetime.today().strftime('%Y-%m-%d')
        posts_by_date = get_posts_by_date(session, "2026-05-28")
        print(f"Количество опубликованных постов за эту дату: {len(posts_by_date)}")

        print("\nЗадание 3: Добавление нескольких авторов")
        authors_add = [("Николай Гоголь", "gogol@example"), ("Антон Чехов", "chehov@example")]
        create_many_authors(session, authors_add)
        print("Авторы добавлены")

        print("\nЗадание 4: Пост и комментарии")
        post_data = get_posts_with_comments(session, post1.id)
        if post_data:
            print(f"Пост: '{post_data.title}'")
            print(f"Комментарии ({len(post_data.comments)}):")
            for comment in post_data.comments:
                print(f"- [{comment.author_name}]: {comment.text}")




    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()
        print("\nТестирование завершено. Сессия закрыта.")


if __name__ == "__main__":
    main()
