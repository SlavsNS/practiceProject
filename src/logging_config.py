import logging

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler("logs.log"),
            logging.StreamHandler()
        ]
    )
    print("Logging configured!")
