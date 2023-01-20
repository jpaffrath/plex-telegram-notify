from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio, telegram, json

### Configure your server here ###
hostName   = YOUR-LOCAL-IP
serverPort = 9000

### Configure your telegram bot here
botID      = YOUR-BOT-ID
chatID     = YOUR-CHAT-ID

class MyServer(BaseHTTPRequestHandler):

    async def send_notify(self, msg):
        bot = telegram.Bot(botID)
        async with bot:
            await bot.send_message(text=msg, chat_id=chatID)

    def handle_mediaPlay(self, account, player, media):
        message = account["title"] + " has started playing " + media["title"] + " on " + player["title"]
        asyncio.run(self.send_notify(message))

    def handle_mediaPause(self, account, player, media):
        pass

    def handle_mediaResume(self, account, player, media):
        pass

    def handle_mediaStop(self, account, player, media):
        message = account["title"] + " has stopped playing " + media["title"] + " on " + player["title"]
        asyncio.run(self.send_notify(message))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])

        # read post bytes from POST request and decode
        post_data = self.rfile.read(content_length)
        post_data_decode = post_data.decode("utf-8", "ignore")

        # get the boundary from header and split the payload
        header_boundary = self.headers.get_boundary()
        post_data_list = post_data_decode.split(header_boundary)

        # trim and parse json payload from second payload object (Plex Webhook sends sometimes an image as third object)
        post_data_payload = post_data_list[1]
        post_payload = post_data_payload[post_data_payload.find("{"):post_data_payload.rfind("}")+1]
        payload = json.loads(post_payload)

        event   = payload["event"]
        account = payload["Account"]
        player  = payload["Player"]
        media   = payload["Metadata"]

        # handle playback events
        if event   == "media.play":
            self.handle_mediaPlay(account, player, media)
        elif event == "media.resume":
            self.handle_mediaResume(account, player, media)
        elif event == "media.pause":
            self.handle_mediaPause(account, player, media)
        elif event == "media.stop":
            self.handle_mediaStop(account, player, media)


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Goodbye!")
