import logging


packages_to_surpass = ["fastapi"]

for package in packages_to_surpass:
    logging.getLogger(package).setLevel(level=logging.INFO)


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
