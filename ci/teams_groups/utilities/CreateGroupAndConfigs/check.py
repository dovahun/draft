from ruamel.yaml import YAML
from ruamel.yaml import YAMLError
import argparse
import glob
from marshmallow import Schema, fields, exceptions
import sys
import os
import logging


class Args:

    def __init__(self):
        arg = argparse.ArgumentParser(description='yaml configuration validation')
        arg.add_argument('-d', required=True, help='users configuration directory path')
        self.arguments = vars(arg.parse_args())


class Logger:

    def __init__(self):
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)


class Files:

    def __init__(self, dir):
        self.files = []
        self.dir = dir
        self.find_files_with_invalid_extension()
        self.find_files_by_extension()

    def find_files_with_invalid_extension(self):
        files = glob.glob(self.dir + '/*')
        for file in files:
            name, ext = os.path.splitext(file)
            if ext in [".yaml", ".md"]:
                continue
            else:
                raise ValueError("Невалидное расширение файла {}".format(file))

    def find_files_by_extension(self):
        files = glob.glob(self.dir + '/*.yaml')
        for file in files:
            self.files.append(file)

class Yml:

    def __init__(self, yml_file):
        try:
            self.yml = YAML(typ='safe')
            self.content = self.yml.load(open(yml_file))
        except YAMLError as e:
            print(e)
            sys.exit(1)


class Team(Schema):
    name = fields.Str()
    state = fields.Str()


if __name__ == '__main__':
    logger = Logger()
    args = Args()
    schema = Team()
    try:
        logger.log.info("Проверка файла на валидность")
        files = Files(args.arguments['d'])
    except ValueError as e:
        logger.log.exception(e)
        sys.exit(1)
    for file in files.files:
        yaml = Yml(file)
        try:
            result = schema.load(yaml.content)
        except exceptions.ValidationError as e:
            logger.log.exception(e)
            sys.exit(1)
        fileName = os.path.basename(file).split('.yaml')[0]
        if fileName != result['name']:
            logger.log.error("Имя файла: {0} и название team: {1} не соответвуют друг другу".format(fileName, result['name']))
            exit(1)
        if not result['name'].endswith("app"):
            logger.log.error("Team: {0} не содержит окончание -app в конце имени, поля name.".format(fileName, result['name']))
            exit(1)
    logger.log.info("Проверка файла завершилась успешно")
    sys.exit(0)
