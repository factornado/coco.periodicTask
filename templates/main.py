import factornado
from tornado import web


class HelloWorld(web.RequestHandler):
    swagger = {
        "path": "/{name}/{uri}",
        "operations": [
            {
                "notes": "Return hello world.",
                "method": "GET",
                "responseMessages": [
                    {"message": "OK", "code": 200},
                    {"message": "Unauthorized", "code": 401},
                    {"message": "Forbidden", "code": 403},
                    {"message": "Not Found", "code": 404}
                    ],
                "deprecated": False,
                "produces": ["application/json"],
                "parameters": []
                }
            ]}
    nb = 0

    def get(self):
        self.write('Hello world nb {}'.format(self.nb))
        self.nb += 1


class Todo(factornado.Todo):
    def todo_loop(self, data):
        for k in range(2):
            data['nb'] += 1
            yield 'ABCDE'[data['nb'] % 5], {}


class Do(factornado.Do):
    def do_something(self, task_key, task_data):
        return 'something'


app = factornado.Application('config.yml', [
    ("/hello", HelloWorld),
    ("/todo", Todo),
    ("/do", Do),
    ], )

if __name__ == '__main__':
    app.start_server()
