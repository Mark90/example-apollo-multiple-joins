import json
import sys
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

AUTHORS = {
    1: {"name": "Bob"},
    2: {"name": "Alice"},
}


@strawberry.federation.type(keys=["id"])
class Author:
    id: int
    name: str

    async def resolve_reference(info: Info, id: int) -> "Author | None":
        payload = await info.context['request'].json()
        print(f"Looking up Author with id={id} request {payload}", file=sys.stderr)
        if not (author := AUTHORS.get(id)):
            return None
        return Author(id=id, **author)


async def get_authors() -> list[Author]:
    return [Author(id=id, **author) for id, author in AUTHORS.items()]


@strawberry.type
class Query:
    authors: list[Author] = strawberry.field(resolver=get_authors)


schema = strawberry.federation.Schema(query=Query, types=[Author], enable_federation_2=True)

graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/api/graphql")
