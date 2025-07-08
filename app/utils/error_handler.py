import logging

logger = logging.getLogger("portfolio-assistant")
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logger.addHandler(console)


def safe_call(fn, fallback=None, context=""):
    try:
        return fn()
    except Exception as e:
        logger.warning(f"Failed during {context}:.{str(e)}")
        return fallback
