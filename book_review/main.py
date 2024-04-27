import asyncio
import sys

import rich.traceback
import uvloop

from book_review.app import run
from book_review.config import settings

# install rich traceback that pretty prints exceptions
rich.traceback.install(show_locals=settings.DEBUG)


def main() -> None:
    # use uvloop as a faster asyncio alternative
    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(run())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    main()
