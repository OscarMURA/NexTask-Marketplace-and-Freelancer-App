import pytest
from django.contrib.auth import get_user_model
from Messaging.models import Thread, Message

User = get_user_model()

@pytest.mark.django_db
def test_thread_creation():
    # Crear usuarios (freelancer y cliente)
    freelancer = User.objects.create_user(username="freelancer", password="freelancer123")
    client = User.objects.create_user(username="client", password="client123")

    # Crear un hilo con ambos usuarios
    thread = Thread.objects.create()
    thread.participants.add(freelancer, client)

    # Comprobar si el hilo se ha creado correctamente
    assert thread.participants.count() == 2
    assert freelancer in thread.participants.all()
    assert client in thread.participants.all()
    assert str(thread) == "Thread between freelancer, client"

@pytest.mark.django_db
def test_message_creation():
    # Crear usuarios
    freelancer = User.objects.create_user(username="freelancer", password="freelancer123")
    client = User.objects.create_user(username="client", password="client123")

    # Crear un hilo y añadir los usuarios
    thread = Thread.objects.create()
    thread.participants.add(freelancer, client)

    # Crear un mensaje enviado por el freelancer
    message = Message.objects.create(thread=thread, sender=freelancer, body="Hello client!")

    # Verificar si el mensaje se ha creado correctamente
    assert message.thread == thread
    assert message.sender == freelancer
    assert message.body == "Hello client!"
    assert str(message) == f"Message from freelancer at {message.timestamp}"

@pytest.mark.django_db
def test_multiple_messages_in_thread():
    # Crear usuarios
    freelancer = User.objects.create_user(username="freelancer", password="freelancer123")
    client = User.objects.create_user(username="client", password="client123")

    # Crear un hilo y añadir los usuarios
    thread = Thread.objects.create()
    thread.participants.add(freelancer, client)

    # Crear múltiples mensajes
    message1 = Message.objects.create(thread=thread, sender=freelancer, body="Hello client!")
    message2 = Message.objects.create(thread=thread, sender=client, body="Hello freelancer!")

    # Verificar si ambos mensajes pertenecen al mismo hilo
    assert thread.messages.count() == 2
    assert message1 in thread.messages.all()
    assert message2 in thread.messages.all()
