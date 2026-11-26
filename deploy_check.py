
import json
import os
import subprocess
import sys
import time
import urllib.request

PORT = os.environ.get("DEPLOY_PORT", "5055")
BASE = f"http://127.0.0.1:{PORT}"


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=3) as res:
        return res.status, res.read().decode()


def wait_until_up(proc, seconds=30):
    for _ in range(seconds):
        if proc.poll() is not None:
            raise RuntimeError("App start hote hi band ho gayi")
        try:
            status, _ = get("/health")
            if status == 200:
                return
        except Exception:
            time.sleep(1)
    raise RuntimeError("App 30 second mein start nahi hui")


def main():
    env = dict(os.environ, PORT=PORT, APP_ENV="production")
    print(f"[deploy] App start ho rahi hai: {BASE} (APP_ENV=production)")
    proc = subprocess.Popen([sys.executable, "app.py"], env=env)
    try:
        wait_until_up(proc)
        print("[deploy] App up hai")

        status, body = get("/health")
        assert status == 200 and json.loads(body)["status"] == "ok", "health check fail"
        print("[deploy] /health OK")

        status, body = get("/")
        assert status == 200 and "Task Manager" in body, "frontend page nahi mila"
        print("[deploy] Frontend (/) OK")

        status, body = get("/api/info")
        assert json.loads(body)["env"] == "production", "environment production nahi hai"
        print("[deploy] /api/info OK (env=production)")

        print("[deploy] Deploy successful")
        return 0
    except Exception as err:
        print(f"[deploy] FAIL: {err}")
        return 1
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("[deploy] App band kar di")


if __name__ == "__main__":
    sys.exit(main())