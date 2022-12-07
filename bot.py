import requests

from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


def get_chatgpt_response(prompt):

    try:
        response = requests.get("http://localhost:5001/chat", params={"q": prompt})
    except Exception as e:
        response = None

    if response and response.status_code == 200:
        return response.text
    return None


def get_email_prompt(text):
    prompt_text = """Can you write a good email for "{context}"? The output should be formatted and should only contain email content."""
    return prompt_text.format(context=text.strip())


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()

    if "email" in incoming_msg.lower():
        msg_stripped = incoming_msg.replace("email", "")
        final_prompt = get_email_prompt(msg_stripped)
    else:
        final_prompt = incoming_msg

    response = get_chatgpt_response(final_prompt)
    resp.message(response)
    return Response(str(resp), mimetype="application/xml")

if __name__ == "__main__":
    app.run(port=4000)
