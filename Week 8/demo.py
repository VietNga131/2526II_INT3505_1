from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 1)
    @task
    def get_posts(self):
        with self.client.get(
            "/posts", 
            catch_response=True
        ) as response:
            if response.status_code == 200:
                duration = response.elapsed.total_seconds()
                if duration < 0.5:
                    response.success()
                else:
                    msg = f"Slow response: {duration}s"
                    response.failure(msg)
            else:
                response.failure(
                    f"HTTP Error: {response.status_code}"
                )


                