from httpx import AsyncClient

from tests.test_auth import register


async def auth_header(client: AsyncClient, email: str = "jane@example.com") -> dict[str, str]:
    response = await register(client, email=email, name="Jane Doe")
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['token']}"}


async def test_books_require_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/books")
    assert response.status_code == 401


async def test_book_crud_is_scoped_to_the_current_user(client: AsyncClient) -> None:
    jane = await auth_header(client, email="jane@example.com")
    john = await auth_header(client, email="john@example.com")

    created = await client.post(
        "/api/v1/books",
        headers=jane,
        json={"title": "Dune", "author": "Frank Herbert", "description": "Arrakis"},
    )
    assert created.status_code == 201
    book = created.json()
    assert book["title"] == "Dune"
    assert book["user_id"] > 0
    book_id = book["id"]

    listing = await client.get("/api/v1/books", headers=jane)
    assert listing.status_code == 200
    assert [row["id"] for row in listing.json()] == [book_id]

    other_listing = await client.get("/api/v1/books", headers=john)
    assert other_listing.json() == []

    hidden = await client.get(f"/api/v1/books/{book_id}", headers=john)
    assert hidden.status_code == 404

    updated = await client.patch(
        f"/api/v1/books/{book_id}",
        headers=jane,
        json={"title": "Dune Messiah", "description": None},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Dune Messiah"
    assert updated.json()["author"] == "Frank Herbert"
    assert updated.json()["description"] is None

    deleted = await client.delete(f"/api/v1/books/{book_id}", headers=jane)
    assert deleted.status_code == 204

    missing = await client.get(f"/api/v1/books/{book_id}", headers=jane)
    assert missing.status_code == 404
