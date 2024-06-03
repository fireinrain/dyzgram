import utils
from logs import logger
from client import tgclient
from config import GLONAL_CONFIG
from telethon import TelegramClient
from auth import auth_by_qrcode, auth_by_tel_code


async def main(client: TelegramClient):
    enable_qrcode_ = GLONAL_CONFIG['telegram']['enable_qrcode']
    if isinstance(enable_qrcode_, str):
        enable_qrcode_ = True
    if enable_qrcode_:
        await auth_by_qrcode(client)
    else:
        await auth_by_tel_code(client)

    me_ = await tgclient.get_me()
    print(me_)


if __name__ == '__main__':
    logger.info("starting running dyzgram client, please wait...")
    tgclient.loop.run_until_complete(main(tgclient))
