from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import sys
import trello_task_manager as ttm

sys.path.append(r'C:\Users\mimib\clawd')

app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get('Body', '').strip()

    resp = MessagingResponse()

    if not incoming_msg:
        resp.message("No message received.")
        return Response(str(resp), mimetype="application/xml")

    try:
        task_added = ttm.add_task_to_do(incoming_msg)
        if task_added:
            resp.message(f"Task added to To Do list: {incoming_msg}")
        else:
            resp.message("Failed to add task.")
    except Exception as e:
        print(f"Error adding task: {e}")
        resp.message("Error processing your task.")

    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(port=5000)
