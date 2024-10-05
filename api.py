from fastapi import FastAPI

import src.api.api as api
import src.utils.logger as logger

log = logger.get_logger('api')

tags_metadata = [
    {
        "name": "health",
        "description": "Validation if service is up and running.",
    },
    {
        "name": "news",
        "description": "Read and search news items.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.include_router(api.router)
