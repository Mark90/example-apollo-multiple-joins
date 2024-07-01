# Usage

```
docker compose up
```

Wait until the services are up and the federated graph has been built and is running. I.e. until you see

> federation-1      | {"timestamp":"2024-07-01T13:24:05.252826422Z","level":"INFO","message":"GraphQL endpoint exposed at http://0.0.0.0:4000/ 🚀","target":"apollo_router::axum_factory::axum_http_server_factory","resource":{"process.executable.name":"router","service.version":"1.47.0","service.name":"unknown_service:router"}}


Then navigate to http://localhost:4000/


## Multiple entities on the same field

Running the query

```graphql
query GetBooksWithAuthor {
  books {
    title
    author {
      id
      name
    }
  }
}
```

Gives as response

```json
{
  "data": {
    "books": [
      {
        "title": "How to cook",
        "author": {
          "id": 1,
          "name": "Bob"
        }
      },
      {
        "title": "How to read",
        "author": {
          "id": 1,
          "name": "Bob"
        }
      },
      {
        "title": "How to code",
        "author": {
          "id": 2,
          "name": "Alice"
        }
      }
    ]
  }
}
```

Logs show author 1 is only retrieved once.

> author-service-1  | Looking up Author with id=1 request {'query': 'query GetBooksWithAuthor__authors__1($representations:[_Any!]!){_entities(representations:$representations){...on Author{name}}}', 'operationName': 'GetBooksWithAuthor__authors__1', 'variables': {'representations': [{'__typename': 'Author', 'id': 1}, {'__typename': 'Author', 'id': 2}]}}
>
> author-service-1  | Looking up Author with id=2 request {'query': 'query GetBooksWithAuthor__authors__1($representations:[_Any!]!){_entities(representations:$representations){...on Author{name}}}', 'operationName': 'GetBooksWithAuthor__authors__1', 'variables': {'representations': [{'__typename': 'Author', 'id': 1}, {'__typename': 'Author', 'id': 2}]}}


## Multiple entities on different fields

Running the query

```graphql
query GetBooksWithAuthorAndCoAuthor {
  books {
    title
    author {
      id
      name
    }
    coAuthor {
      id
      name
    }
  }
}
```

Gives the response

```json
{
  "data": {
    "books": [
      {
        "title": "How to cook",
        "author": {
          "id": 1,
          "name": "Bob"
        },
        "coAuthor": {
          "id": 2,
          "name": "Alice"
        }
      },
      {
        "title": "How to read",
        "author": {
          "id": 1,
          "name": "Bob"
        },
        "coAuthor": null
      },
      {
        "title": "How to code",
        "author": {
          "id": 2,
          "name": "Alice"
        },
        "coAuthor": null
      }
    ]
  }
}
```

Logs show author 2 is now retrieved twice.

> author-service-1  | Looking up Author with id=1 request {'query': 'query GetBooksWithAuthorAndCoAuthor__authors__1($representations:[_Any!]!){_entities(representations:$representations){...on Author{name}}}', 'operationName': 'GetBooksWithAuthorAndCoAuthor__authors__1', 'variables': {'representations': [{'__typename': 'Author', 'id': 1}, {'__typename': 'Author', 'id': 2}]}}
>
> author-service-1  | Looking up Author with id=2 request {'query': 'query GetBooksWithAuthorAndCoAuthor__authors__1($representations:[_Any!]!){_entities(representations:$representations){...on Author{name}}}', 'operationName': 'GetBooksWithAuthorAndCoAuthor__authors__1', 'variables': {'representations': [{'__typename': 'Author', 'id': 1}, {'__typename': 'Author', 'id': 2}]}}
>
> author-service-1  | Looking up Author with id=2 request {'query': 'query GetBooksWithAuthorAndCoAuthor__authors__2($representations:[_Any!]!){_entities(representations:$representations){...on Author{name}}}', 'operationName': 'GetBooksWithAuthorAndCoAuthor__authors__2', 'variables': {'representations': [{'__typename': 'Author', 'id': 2}]}}

