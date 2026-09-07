import json
import logging
import re

_SENSITIVE_VALUE = re.compile(
    r"(?i)(password|secret|token|authorization)(\s*[=:]\s*)([^\s,;]+)"
)


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = _SENSITIVE_VALUE.sub(r"\1\2[REDACTED]", record.getMessage())
        return json.dumps(
            {
                "timestamp": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "logger": record.name,
                "message": message,
            },
            ensure_ascii=False,
        )


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter("%(levelname)s %(name)s %(message)s"))
    logging.basicConfig(level=level, handlers=[handler], force=True)
