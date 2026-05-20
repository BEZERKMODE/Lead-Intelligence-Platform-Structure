import time
import logging

from fastapi import Request

logger = logging.getLogger(__name__)

async def request_logger(
    request: Request,
    call_next
):

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"{request.method} {request.url} took {duration}"
    )

    return response
