from locust import HttpUser, task, between

class NotepadUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """
        Este método se ejecuta para cada usuario para que inicie sesión.
        """
        print("Iniciando sesión de un nuevo usuario...")
        login_response = self.client.post("/login", {
            "email": "user1@example.com",
            "password": "1234"
        })
        if login_response.status_code == 200:
            print("Login exitoso.")
        else:
            print(f"Fallo en el login: {login_response.status_code}")

    @task(2)
    def load_notepads(self):
        print("Cargando la lista de notas...")
        response = self.client.get("/notepad")
        if response.status_code == 200:
            print("Lista de notas cargada correctamente.")
        else:
            print(f"Error al cargar la lista de notas: {response.status_code}")

    @task(1)
    def create_notepad(self):
        print("Creando una nueva nota...")
        response = self.client.post(
            "/notepad/create",
            data={
                "title": "Nota creada por Locust",
                "body": "Cuerpo de la nota de prueba."
            }
        )
        if response.status_code == 302:
            print("Nota creada correctamente.")
        else:
            print(f"Error al crear la nota: {response.status_code}")
