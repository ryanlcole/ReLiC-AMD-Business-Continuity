from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow direct execution from the repository root without requiring installation.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.relic.observation import observe_aws_control


def main() -> None:
    record = observe_aws_control(
        [{"role": "user", "content": "Return exactly: RELIC_AWS_OBSERVE_PASS"}]
    )
    print(json.dumps(record.as_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
