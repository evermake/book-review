from random import randint

from locust import FastHttpUser, between, task


class UnauthorizedUser(FastHttpUser):
    wait_time = between(3, 8)

    @task
    def search_books(self):
        for query in [
            "Don Quixote",
            "The Little Prince",
            "War and Peace",
            "A Tale of Two Cities",
        ]:
            self.client.get("/books", params={"query": query})

    @task
    def search_users(self):
        self.client.get("/users")

    @task
    def get_me(self):
        with self.client.get("/users/me", catch_response=True) as response:
            if response.status_code == 401:
                response.success()

    @task
    def get_reviews(self):
        self.client.get("/reviews")

    @task
    def create_review(self):
        with self.client.post(
            "/reviews",
            data={"rating": randint(1, 10), "book_id": "bla bla"},
            catch_response=True,
        ) as response:
            if response.status_code == 401:
                response.success()
