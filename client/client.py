from config import GLONAL_CONFIG
from logs import logger

tgclient = None
sentry_ex_reporter = None

_nickname = GLONAL_CONFIG['telegram']['nickname']
_app_id = GLONAL_CONFIG['telegram']['app_id']
_app_hash = GLONAL_CONFIG['telegram']['app_hash']

_enable_proxy = GLONAL_CONFIG['proxy']['enable']
_proxy_mode = GLONAL_CONFIG['proxy']['mode']
_proxy_config = GLONAL_CONFIG['proxy']['type'][_proxy_mode]

# sentry exceptions report
_sentry_enable = GLONAL_CONFIG['sentry']['enable']
_sentry_dsn = GLONAL_CONFIG['sentry']['dsn']

if _sentry_enable:
    import sentry_sdk

    sentry_ex_reporter = sentry_sdk.init(
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
    logger.info("Sentry ex reporter is enabled and started.")

if _enable_proxy and _proxy_mode in ['socks', 'http', 'mtproxy']:
    pass

    logger.info(f"Use proxy for dyzgram client: {_proxy_mode}:{_proxy_config}")
