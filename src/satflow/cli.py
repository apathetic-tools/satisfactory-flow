import logging


# --------------------------------------------------------------------------- #
# Main entry
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:  # noqa: ARG001
    logger = logging.getLogger(__name__)
    logger.info("Hello, World!")
    return 0
