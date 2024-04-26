from random import randint
from uuid import uuid4

from locust import FastHttpUser, task


class UnauthorizedUser(FastHttpUser):
    @task
    def search_books(self) -> None:
        self.client.get("/books", params={"query": "Don Quixote"})

    @task
    def search_users(self) -> None:
        self.client.get("/users")

    @task
    def get_me(self) -> None:
        with self.client.get("/users/me", catch_response=True) as response:
            if response.status_code == 401:
                response.success()

    @task
    def get_reviews(self) -> None:
        self.client.get("/reviews")

    @task
    def create_review(self) -> None:
        with self.client.post(
            "/reviews",
            data={"rating": randint(1, 10), "book_id": str(uuid4())},
            catch_response=True,
        ) as response:
            if response.status_code == 401:
                response.success()
