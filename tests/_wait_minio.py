"""Wait for the private CI S3 fixture, failing closed after 60 seconds."""

import time
import urllib.error
import urllib.request


def wait_ready(timeout=60):
    deadline = time.monotonic() + timeout
    while True:
        try:
            with urllib.request.urlopen(
                "http://minio:9000/minio/health/ready", timeout=2
            ) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError):
            pass
        if time.monotonic() >= deadline:
            raise RuntimeError("MinIO fixture did not become ready")
        time.sleep(1)


if __name__ == "__main__":
    wait_ready()
