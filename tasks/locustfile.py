from locust import HttpLocust, TaskSet, task

class ExampleTasks(TaskSet):
    @task(1)
    def hello(self):
        self.client.get("/hello")

class Example(HttpLocust):
    task_set = ExampleTasks
    min_wait = 5000
    max_wait = 10000
