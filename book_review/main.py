import asyncio
import sys

import rich.traceback
import uvloop

from book_review.app import App
from book_review.config import settings

rich.traceback.install(show_locals=settings.DEBUG)


def main() -> None:
    app = App()

    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(app.run())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    main()
