from flask import Blueprint, request, Response, jsonify
from app.services.twilio_service import send_whatsapp_message, handle_incoming_message

webhook = Blueprint('webhook', __name__)

@webhook.route('/webhook', methods=['POST'])
def receive_message():
    try:
        sender = request.form.get('From')
        message_body = request.form.get('Body')

        if not sender or not message_body:
            return jsonify({'error': 'Invalid input'}), 400

        sender = sender.split(':')[1]
        response = handle_incoming_message(message_body, sender)
        send_whatsapp_message(sender, response)

        return Response(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500