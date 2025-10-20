import pytest

from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout
from app.modules.notepad.models import Notepad


@pytest.fixture(scope="module")
def test_client(test_client):
    with test_client.application.app_context():
        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        notepad = Notepad(title="Nota de Prueba", body="Contenido de la nota.", user_id=user_test.id)
        db.session.add(notepad)
        db.session.commit()

    yield test_client


def test_notepad_page_get(test_client):
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "El login falló."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "No se pudo acceder a la página de notas."
    
    assert b"Nota de Prueba" in response.data, "La nota del usuario no aparece en la página."

    logout(test_client)

