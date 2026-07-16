import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("app.log"),   # Save logs to a file
        logging.StreamHandler()           # Also print to the terminal
    ]
)