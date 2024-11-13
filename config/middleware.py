from fastapi import Request
import time
import logging

async def log_requests(request: Request, call_next):
    """Custom logging middleware for structured and centralized logging."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logging.info(f"{request.method} {request.url} completed in {process_time:.2f}s")
    return response
