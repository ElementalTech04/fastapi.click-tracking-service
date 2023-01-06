from fastapi import FastAPI, Request, BackgroundTasks, Depends
from fastapi.responses import RedirectResponse;
import aioredis
from aioredis.exceptions import ResponseError
import logging
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pydantic import BaseSettings
import functools


DEFAULT_KEY_PREFIX = 'is-bitcoin-lit'
TWO_MINUTES = 60 + 60
HOURLY_BUCKET = '3600000'

class Keys:
    """Methods to generate key names for Redis data structures."""

    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def timeseries_ping_key(self) -> str:
        """A time series containing 30-second snapshots of url hits."""
        return f'ping:mean:30s'

    @prefixed_key
    def cache_key(self) -> str:
        return f'cache'


class Config(BaseSettings):
    # The default URL expects the app to run using Docker and docker-compose.
    redis_url: str = os.getenv("REDIS_CONN_URL")


log = logging.getLogger(__name__)
config = Config()
app = FastAPI(title='FastAPI Redis Tutorial')
redis = aioredis.from_url(config.redis_url, decode_responses=True)


class RedirectPair(BaseModel):
    id: int
    redirectUrl: str
    shortUrl:str


app.get("/")
async def landingMethod(source: string, request: Request):
    logRequestDetails(source, request)
    redirectUrl = await findRedirectUrl(request)
    return RedirectResponse(url=redirectUrl, status_code=status.HTTP_303_SEE_OTHER)

app.get("/register")
def getRegisterRecords():
    return {'hooo', 'heeyyyy'}

app.post("/register")
def postNewRegisterRecord(record: RedirectPair):
    return {'hooo', 'heeyyyy'}


# Services

def logRequestDetails(source: string, request: Request) -> None:
    return 
    

def findRedirectUrl(request: Request, keys: Keys) -> str:
    
    return redi


async def add_many_to_timeseries(
    key_pairs: Iterable[Tuple[str, str]],
    redirectUrl: str
):
    """
    Add many samples to a single timeseries key.
    `key_pairs` is an iteratble of tuples containing in the 0th position the
    timestamp key into which to insert entries and the 1th position the name
    of the key within th `data` dict to find the sample.
    """
    partial = functools.partial(redis.execute_command, 'TS.MADD')
    for datapoint in data:
        for timeseries_key, sample_key in key_pairs:
            partial = functools.partial(
                partial, timeseries_key, int(
                    float(datapoint['timestamp']) * 1000,
                ),
                datapoint[sample_key],
            )
    return await partial()


def make_keys():
    return Keys()


async def persist(keys: Keys, data: BitcoinSentiments):
    ts_sentiment_key = keys.timeseries_sentiment_key()
    ts_price_key = keys.timeseries_price_key()
    await add_many_to_timeseries(
        (
            (ts_price_key, 'btc_price'),
            (ts_sentiment_key, 'mean'),
        ), data,
    )
    
async def get_cache(keys: Keys):
    current_hour_cache_key = keys.cache_key()
    current_hour_stats = await redis.get(current_hour_cache_key)

    if current_hour_stats:
        return json.loads(current_hour_stats, object_hook=datetime_parser)


async def set_cache(data, keys: Keys):
    def serialize_dates(v):
        return v.isoformat() if isinstance(v, datetime) else v

    await redis.set(
        keys.cache_key(),
        json.dumps(data, default=serialize_dates),
        ex=TWO_MINUTES,
    )
    
async def initialize_redis(keys: Keys):
    await make_timeseries(keys.timeseries_ping_key()())

#On Startup
@app.on_event('startup')
async def startup():
    keys = Keys()
    await initialize_redis(keys)
