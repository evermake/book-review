import asyncio
import sys

import uvicorn
import uvloop

from book_review.config import settings
from book_review.ui.http_app import app


async def run() -> None:
    config = uvicorn.Config(app, port=settings.PORT, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


def main() -> None:
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(run())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    main()
