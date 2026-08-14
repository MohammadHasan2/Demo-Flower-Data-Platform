import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from reports.telegram import send_telegram_message


def send_failure_notification(error):

    message = f"""
🚨 ZeeFlower ETL Failed
━━━━━━━━━━━━━━━━━━━━

❌ Status: FAILED

Error:
{error}

⚠️ Daily report was not generated.
""".strip()

    send_telegram_message(message)


if __name__ == "__main__":
    send_failure_notification(
        "Test ETL failure notification"
    )