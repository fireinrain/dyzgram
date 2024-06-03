import python_socks
from telethon import TelegramClient
from telethon.network import connection

from config import GLONAL_CONFIG
from logs import logger

tgclient = None
_sentry_reporter = None

_nickname = GLONAL_CONFIG['telegram']['nickname']
_api_id = GLONAL_CONFIG['telegram']['api_id']
_api_hash = GLONAL_CONFIG['telegram']['api_hash']

_enable_proxy = GLONAL_CONFIG['proxy']['enable']
_proxy_mode = GLONAL_CONFIG['proxy']['mode']
_proxy_config = GLONAL_CONFIG['proxy']['type'][_proxy_mode]

# sentry exceptions report
_sentry_enable = GLONAL_CONFIG['sentry']['enable']
_sentry_dsn = GLONAL_CONFIG['sentry']['dsn']

if _sentry_enable:
    import sentry_sdk

    _sentry_reporter = sentry_sdk.init(
        dsn=_sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
    sentry_sdk.capture_message(">>>: success enable sentry ex reporter.")
    logger.info("Sentry reporter is enabled and started.")

if _enable_proxy and _proxy_mode in ['socks', 'http', 'mtproxy']:
    if _proxy_mode == 'socks':
        socks_config = GLONAL_CONFIG['proxy']['type'][_proxy_mode]
        proxy = None
        # socks need auth
        proxy = {
            'proxy_type': python_socks.ProxyType.SOCKS5,
            'addr': socks_config['host'],
            'port': socks_config['port'],
            'rdns': True  # (optional) whether to use remote or local resolve, default remote
        }
        if socks_config['username'] != "":
            # don't need auth
            proxy.update({'username': socks_config['username'],
                          'password': socks_config['password']})

        tgclient = TelegramClient(
            _nickname,
            _api_id,
            _api_hash,
            proxy=proxy,
        )

    elif _proxy_mode == 'http':
        socks_config = GLONAL_CONFIG['proxy']['type'][_proxy_mode]

        proxy = {
            'proxy_type': python_socks.ProxyType.SOCKS5,
            'addr': socks_config['host'],
            'port': socks_config['port'],
        }
        tgclient = TelegramClient(
            _nickname,
            _api_id,
            _api_hash,
            proxy=proxy,
        )

    elif _proxy_mode == 'mtproxy':
        socks_config = GLONAL_CONFIG['proxy']['type'][_proxy_mode]
        proxy = (socks_config['host'], socks_config['port'], socks_config['secret'])
        tgclient = TelegramClient(
            _nickname,
            _api_id,
            _api_hash,

            # Use one of the available connection modes.
            # Normally, this one works with most proxies.
            connection=connection.ConnectionTcpMTProxyRandomizedIntermediate,

            # Then, pass the proxy details as a tuple:
            #     (host name, port, proxy secret)
            #
            # If the proxy has no secret, the secret must be:
            #     '00000000000000000000000000000000'
            proxy=proxy,
        )

    logger.info(f"Use proxy for dyzgram client: {_proxy_mode}:{_proxy_config}")

else:
    tgclient = TelegramClient(
        _nickname,
        _api_id,
        _api_hash,
    )
    logger.info(f"Use direct connect for dyzgram client: {_proxy_mode}:{_proxy_config}")


class Sentry(object):
    def __init__(self, sentry_obj):
        self.sentry_obj = sentry_obj

    def report_exception(self, exception):
        if self.sentry_obj is None:
            pass
        else:
            self.sentry_obj.capture_exception(exception)

    def report_message(self, message):
        if self.sentry_obj is None:
            pass
        else:
            self.sentry_obj.capture_message(message)


sentry_reporter = Sentry(_sentry_reporter)

