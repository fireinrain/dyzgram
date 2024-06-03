from telethon import TelegramClient
from logs import logger
import utils


async def auth_by_qrcode(client: TelegramClient):
    logger.info("Auth login telegram by QRCode.")
    if not client.is_connected():
        await client.connect()
    await client.connect()
    # Ensure the client is not already logged in
    if not await client.is_user_authorized():
        # Generate the QR code
        login_token = await client.qr_login()
        logger.info(f"Telethon client connect status: {client.is_connected()}")
        logger.info("Please scan the QR code with your Telegram app to log in.")
        qr_login_finish = False

        while not qr_login_finish:
            logger.info(f"Telegram auth link: {login_token.url}")
            utils.display_url_as_qrcode(login_token.url)
            # Important! You need to wait for the login to complete!
            logger.info(f"Please scan the auth QRCode as quick as possible, it will be refreshed in 30s")
            try:
                qr_login_finish = await login_token.wait(30)
            except TimeoutError:
                await login_token.recreate()


async def auth_by_tel_code(client: TelegramClient):
    logger.info("Auth login telegram by Phone Code.")
    await client.start()
