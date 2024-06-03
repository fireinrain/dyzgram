from logs import logger
from client import tgclient


async def main():
    me = await tgclient.get_me()
    print(me.stringify())


if __name__ == '__main__':
    logger.info("starting running dyzgram client, please wait...")

    with tgclient:
        tgclient.loop.run_until_complete(main())
