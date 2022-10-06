import json
import pika
import django
import os
import sys
from django.core.mail import send_mail
import time
from pika.exceptions import AMQPConnectionError


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    contact = json.loads(body)
    send_mail(
        "Your presentation has been accepted",
        f"{contact['presenter_name']}, we're happy to tell you that your presentation {contact['title']} has been accepted",
        "admin@confernce.go",
        [f"{contact['presenter_email']}"],
        fail_silently=False,
    )


def process_rejections(ch, method, properties, body):
    contact = json.loads(body)
    send_mail(
        "Your presentation has been rejected",
        f"{contact['presenter_name']}, we're happy to tell you that your presentation {contact['title']} has been rejected",
        "admin@confernce.go",
        [f"{contact['presenter_email']}"],
        fail_silently=False,
    )


while True:
    try:
        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue="presentation_approvals")
        channel.queue_declare(queue="presentation_rejections")
        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval,
            auto_ack=True,
        )

        channel.basic_consume(
            queue="presentation_rejections",
            on_message_callback=process_rejections,
            auto_ack=True,
        )

        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
