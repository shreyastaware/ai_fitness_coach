from fastapi import FastAPI, WebSocket
from fastapi.responses import Response
import base64
import json
import uvicorn

app = FastAPI()


# @app.route("/twiml", methods=['POST'])
# def twiml():
#     resp = VoiceResponse()
#     connect = Connect()
#     connect.stream(url="wss://a511462199ba.ngrok-free.app/media")
#     resp.append(connect)
#     return Response(str(resp), mimetype='text/xml')


@app.websocket("/media")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        msg = await websocket.receive_text()
        data = json.loads(msg)
        if data["event"] == "media":
            audio_chunk = base64.b64decode(data["media"]["payload"])
            # process audio here
        elif data["event"] == "stop":
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
