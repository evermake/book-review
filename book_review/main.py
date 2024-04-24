import asyncio
import sys

import uvloop

from book_review.app import App


def main() -> None:
    App.setup()

    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(App.run())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    main()
