from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    def on_start(self):
        response = self.client.post(
            url='/accounts/api/v1/jwt/create/',
            data={
                "email": 'test.test@test.mail',
                "password": 'testPassword@12',
            }
        ).json()

        self.client.headers.update(
            {
                'Authorization': f'Bearer {response.get('access')}'
            }
        )

    @task
    def get_task_list(self):
        self.client.get('/api/v1/tasks/')
