"""Install a version-pinned upstream OPA binary inside an explicit local directory."""
import hashlib
import json
import os
import platform
import tempfile
import urllib.request
from pathlib import Path


def install(destination):
    lock = json.loads(Path(__file__).with_name("opa-lock.json").read_text())
    target = f"{platform.system().lower()}-{platform.machine().lower()}"
    asset, checksum = lock["assets"][target]
    directory = Path(destination).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / ("opa.exe" if platform.system() == "Windows" else "opa")
    if output.exists() and hashlib.sha256(output.read_bytes()).hexdigest() == checksum:
        return output
    url = f"https://github.com/open-policy-agent/opa/releases/download/v{lock['version']}/{asset}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(150_000_001)
    if len(data) > 150_000_000 or hashlib.sha256(data).hexdigest() != checksum:
        raise RuntimeError("OPA checksum mismatch; refusing installation")
    fd, temporary = tempfile.mkstemp(dir=directory)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.chmod(temporary, 0o755)
        os.replace(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return output
