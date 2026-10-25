"""Source-built, CI-only S3 fixture; the retired upstream images are unavailable."""

import subprocess
from pathlib import Path

MINIO_SOURCE_COMMIT = "9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a"
MINIO_IMAGE = "frappe-minio-ci:" + MINIO_SOURCE_COMMIT[:12]


def ensure_minio_fixture():
    result = subprocess.run(
        ("docker", "image", "inspect", MINIO_IMAGE),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode:
        context = Path(__file__).resolve().parent / "minio"
        subprocess.check_call(("docker", "build", "--tag", MINIO_IMAGE, str(context)))
    return MINIO_IMAGE
