import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

BOOKS = [
    {"title": "How to cook", "author": {"id": 1}, "co_author": {"id": 2}},
    {"title": "How to read", "author": {"id": 1}},
    {"title": "How to code", "author": {"id": 2}},
]


@strawberry.federation.type(keys=["id"])
class Author:
    id: int

@strawberry.type
class Book:
    title: str
    author: Author
    co_author: Author | None


async def get_books() -> list[Book]:
    def format_book(dikt: dict) -> Book:
        author = Author(id=dikt['author']['id'])
        co_author = Author(id=dikt['co_author']['id']) if 'co_author' in dikt else None
        return Book(title=dikt['title'], author=author, co_author=co_author)


    return [format_book(book) for book in BOOKS]


@strawberry.type
class Query:
    books: list[Book] = strawberry.field(resolver=get_books)


schema = strawberry.federation.Schema(query=Query, types=[Author], enable_federation_2=True)

graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/api/graphql")
