import utils
from logs import logger
from client import tgclient

from telethon import TelegramClient
from telethon.errors import TimeoutError


async def main(client: TelegramClient):
    if not client.is_connected():
        await client.connect()
    else:
        await client.connect()

    # Ensure the client is not already logged in
    if not await client.is_user_authorized():
        # Generate the QR code
        login_token = await client.qr_login()
        logger.info(f"Telethon client connect status: {client.is_connected()}")
        print("Please scan the QR code with your Telegram app to log in.")
        qr_login_finish = False

        while not qr_login_finish:
            utils.display_url_as_qrcode(login_token.url)
            # Important! You need to wait for the login to complete!
            try:
                qr_login_finish = await login_token.wait(30)
            except TimeoutError:
                await login_token.recreate()
    me_ = await tgclient.get_me()
    print(me_)


if __name__ == '__main__':
    logger.info("starting running dyzgram client, please wait...")

    with tgclient:
        tgclient.loop.run_until_complete(main(tgclient))
