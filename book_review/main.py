import asyncio
import sys

import uvloop

from book_review.app import run


def main() -> None:
    try:
        # use uvloop as a faster asyncio alternative
        if sys.version_info >= (3, 11):
            with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
                runner.run(run())
        else:
            uvloop.install()
            asyncio.run(main())
    except KeyboardInterrupt:
        # TODO: some message maybe?
        pass


if __name__ == "__main__":
    main()
