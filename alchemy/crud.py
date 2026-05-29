from sqlalchemy.orm import Session
from models import Author, Post, Comment
from datetime import datetime, date
from sqlalchemy import func, Date

def create_author(session: Session, name: str, email: str) -> Author:
    """Создает нового автора, возращает объект"""
    new_author = Author(name=name, email=email)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author

def get_author_by_email(session: Session, email: str) -> Author | None:
    """Ищет автора по email"""
    return session.query(Author).filter(Author.email == email).first()

def create_post(session: Session, title: str, content: str,
                author_id: int, published: bool = False) -> Post:
    """Создает новый пост"""
    new_post = Post(title=title, content=content,
                    author_id=author_id, published=published)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

def get_published_posts(session: Session, limit: int = 10) -> list[Post]:
    """Возвращает только опцбикованные посты (published=True)"""
    return session.query(Post).filter(Post.published == True).limit(limit).all()

def get_posts_by_author(session: Session, author_id: int, limit: int = 10)-> list[Post]:
    """Возвращает все посты конкретного автора"""
    return session.query(Post).filter(Post.author_id == author_id).limit(limit).all()

def update_post_status(session: Session, post_id: int, published: bool) -> bool:
    """Меняет статус публикации постаб возвращает Ture если успешно"""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post is None:
        return False #Пост не найден

    post.published = published
    session.commit()
    return True

def add_comment(session: Session, post_id: int, author_name: str, text: str) -> Comment:
    """Добавляет комментарий к посту"""
    new_comment = Comment(post_id=post_id,
                          author_name=author_name, text=text)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

def get_top_authors_by_posts(session: Session, limit: int = 3) -> list[tuple[str,int]]:
    """Возвращает топ авторов по количеству постов.
     Пример возврата: [('Анна', 12), ('Иван", 8), ('Мария', 5)]"""
    from sqlalchemy import func, desc
    #Запрос с агрегацией: считаем количесвто постов для каждого автора
    result = (session.query(Author.name, func.count(Post.id).label('post_count'))

    .join(Post)
    .group_by(Author.id)
    .order_by(desc('post_count'))
    .limit(limit)
    .all())
    return result

def get_author_by_name(session: Session, name: str) -> Author | None:
    return session.query(Author).filter(Author.name == name).first()

def get_posts_by_date(session: Session, date_str: str) -> list[Post]:
    my_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return session.query(Post).filter(Post.created_at.cast(Date) == my_date).all()

def create_many_authors(session: Session, authors_data: list[tuple[str, str]]) -> None:
    for name, email in authors_data:
        new_author = Author(name=name, email=email)
        session.add(new_author)
    session.commit()

def get_posts_with_comments(session: Session, post_id: int) -> Post | None:
    return session.query(Post).filter(Post.id == post_id).first()
