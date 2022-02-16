import argparse
import logging
import math
import re
from importlib import resources
from pathlib import Path

import imageio
import yaml

config = {}


def parse_args():
    parser = argparse.ArgumentParser(description="Transform images from a directory to a GIF.")
    parser.add_argument('source_directory', help="Source directory containing the images.")
    parser.add_argument('output_file', help="Name of the output file.")
    parser.add_argument('--debug', action='store_true', help="Enable debug logging.")
    return parser.parse_args()


def load_config():
    with resources.open_text("image2gif", "default_config.yml") as config_stream:
        config.update(yaml.load(config_stream, yaml.SafeLoader))
    logging.info("Configuration : %s", config)


def get_duration(file: Path):
    if match := re.match(r'\w*_(\d+)', file.stem):
        return int(match.group(1))
    return 100 * config['IMAGE2GIF']['default_duration_in_seconds']


def convert(source_directory: Path, output_file: Path):
    image_files = list(source_directory.iterdir())
    image_files.sort(key=lambda file: file.stem)

    durations = [get_duration(file) for file in image_files]
    smallest_duration = math.gcd(*durations)

    speed_factor = config['IMAGE2GIF']['speed_factor']

    with imageio.get_writer(output_file, mode='I', duration=smallest_duration / 100 / speed_factor) as writer:
        for file, duration in zip(image_files, durations):
            logging.info("Adding %s", file.name)
            image = imageio.imread(file)
            for _ in range(duration // smallest_duration):
                writer.append_data(image)


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    logging.debug("Arguments : %s", args)
    load_config()

    source_directory = Path(args.source_directory)
    output_file = Path(args.output_file)

    convert(source_directory, output_file)


if __name__ == "__main__":
    main()
