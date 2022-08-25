from flask import Config


def print_banner(config: Config) -> None:
    with open("banner.txt", "r") as banner:
        print(banner.read().format(config["VERSION"]))
