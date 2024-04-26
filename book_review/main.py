import asyncio
import sys

import uvloop

from book_review.app import App


def main() -> None:
    app = App()
    app.setup()

    if sys.version_info >= (3, 11):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(app.run())
    else:
        uvloop.install()
        asyncio.run(main())


if __name__ == "__main__":
    main()
