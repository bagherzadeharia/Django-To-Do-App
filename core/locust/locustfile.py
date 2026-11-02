from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        response = self.client.post(
            url='/accounts/api/v1/jwt/create/',
            json={
                "email": 'test.test@test.mail',
                "password": 'testPassword@12',
            }
        )

        if response.status_code == 200:
            try:
                data = response.json()
                access_token = data.get('access')
                if access_token:
                    self.client.headers.update({
                        'Authorization': f'Bearer {access_token}'
                    })
                else:
                    print("Token 'access' not found in response:", data)
            except Exception as e:
                print(f"Error parsing JSON: {e}, Response text was: {response.text}")
        else:
            print(f"Login failed! Status code: {response.status_code}")
            print(f"Response body: {response.text}")

    @task
    def get_task_list(self):
        self.client.get('/api/v1/tasks/')
