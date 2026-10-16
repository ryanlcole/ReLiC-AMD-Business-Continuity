from __future__ import annotations

import json

from app.relic.observation import observe_aws_control


def main() -> None:
    record = observe_aws_control(
        [{"role": "user", "content": "Return exactly: RELIC_AWS_OBSERVE_PASS"}]
    )
    print(json.dumps(record.as_dict(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
