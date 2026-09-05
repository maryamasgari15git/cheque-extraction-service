import asyncio
from functools import wraps


def retry_async(
    max_attempts: int = 3,
    delays: tuple[int, ...] = (2, 5)
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)

                except Exception as e:
                    last_exception = e

                    if attempt == max_attempts - 1:
                        raise

                    delay = delays[min(attempt, len(delays) - 1)]

                    print(
                        f"[RETRY] {type(e).__name__}: "
                        f"attempt {attempt + 1}/{max_attempts}. "
                        f"Retrying in {delay}s..."
                    )

                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper

    return decorator