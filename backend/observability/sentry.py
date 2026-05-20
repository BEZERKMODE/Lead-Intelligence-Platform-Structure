import sentry_sdk

def initialize_sentry(dsn):

    sentry_sdk.init(
        dsn=dsn,
        traces_sample_rate=1.0
    )
