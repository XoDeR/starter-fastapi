from httpx import AsyncClient

REGISTER_BODY = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "secret-password",
    "password_confirmation": "secret-password",
}


async def register(client: AsyncClient, **overrides: str):
    body = {**REGISTER_BODY, **overrides}
    if "email" in overrides and "password_confirmation" not in overrides and "password" not in overrides:
        body["password_confirmation"] = body["password"]
    return await client.post("/api/v1/register", json=body)


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_register_and_read_current_user(client: AsyncClient) -> None:
    response = await register(client, email="Jane@Example.com")
    assert response.status_code == 201
    payload = response.json()
    assert payload["token_type"] == "Bearer"
    assert payload["token"]
    assert "password" not in payload["user"]
    assert payload["user"]["email"] == "jane@example.com"
    assert payload["user"]["name"] == "Jane Doe"

    me = await client.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {payload['token']}"},
    )
    assert me.status_code == 200
    assert me.json()["id"] == payload["user"]["id"]
    assert "password" not in me.json()


async def test_register_rejects_duplicate_email(client: AsyncClient) -> None:
    first = await register(client)
    assert first.status_code == 201
    second = await register(client)
    assert second.status_code == 409


async def test_register_rejects_password_mismatch(client: AsyncClient) -> None:
    response = await register(client, password_confirmation="different-password")
    assert response.status_code == 422


async def test_register_rejects_short_password(client: AsyncClient) -> None:
    response = await register(client, password="short", password_confirmation="short")
    assert response.status_code == 422


async def test_login_returns_token(client: AsyncClient) -> None:
    await register(client)
    response = await client.post(
        "/api/v1/login",
        json={"email": "JANE@example.com", "password": "secret-password"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "Bearer"
    assert body["user"]["email"] == "jane@example.com"


async def test_login_rejects_unknown_email_and_wrong_password(client: AsyncClient) -> None:
    await register(client)
    wrong_password = await client.post(
        "/api/v1/login",
        json={"email": "jane@example.com", "password": "wrong-password"},
    )
    unknown_email = await client.post(
        "/api/v1/login",
        json={"email": "missing@example.com", "password": "secret-password"},
    )
    assert wrong_password.status_code == 401
    assert unknown_email.status_code == 401
    assert wrong_password.json()["detail"] == unknown_email.json()["detail"]


async def test_user_route_requires_a_valid_token(client: AsyncClient) -> None:
    missing = await client.get("/api/v1/user")
    invalid = await client.get("/api/v1/user", headers={"Authorization": "Bearer not-a-token"})
    assert missing.status_code == 401
    assert invalid.status_code == 401
