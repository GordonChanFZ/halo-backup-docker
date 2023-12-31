# encoding:utf-8

import json
import logging
import os
from utils import logger

# 将所有可用的配置项写在字典里, 请使用小写字母
# 此处的配置值无实际意义，程序不会读取此处的配置，仅用于提示格式，请将配置加入到config.json中
available_setting = {
    "website":"", #website你的网站地址，不要带结尾反斜杠
    "backup_halo_path":"/app/backups",#backup_halo_path 通过挂载Halo备份的目录，与挂载目录一致即可
    "ali_folder":"",#ali_folder 你要备份到的阿里云网盘目录ID(网页进入目录后有)
    "user":"",#user 你Halo的账号
    "password":"",#password 你Halo的密码
    "webhook":""#企业微信机器人webhook（可选）
}


class Config(dict):
    def __init__(self, d=None):
        super().__init__()
        if d is None:
            d = {}
        for k, v in d.items():
            self[k] = v


    def __getitem__(self, key):
        if key not in available_setting:
            raise Exception("key {} not in available_setting".format(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key not in available_setting:
            raise Exception("key {} not in available_setting".format(key))
        return super().__setitem__(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError as e:
            return default
        except Exception as e:
            raise e


config = Config()


def load_config():
    global config
    config_path = "./data/config.json"
    if not os.path.exists(config_path):
        logger.info("配置文件不存在，将使用config-template.json模板")
        config_path = "./config-template.json"

    config_str = read_file(config_path)
    logger.debug("[INIT] config str: {}".format(config_str))

    # 将json字符串反序列化为dict类型
    config = Config(json.loads(config_str))

    # override config with environment variables.
    # Some online deployment platforms (e.g. Railway) deploy project from github directly. So you shouldn't put your secrets like api key in a config file, instead use environment variables to override the default config.
    for name, value in os.environ.items():
        name = name.lower()
        if name in available_setting:
            logger.debug("[INIT] override config by environ args: {}={}".format(name, value))
            try:
                config[name] = eval(value)
            except:
                if value == "false":
                    config[name] = False
                elif value == "true":
                    config[name] = True
                else:
                    config[name] = value

    logger.info("[INIT] load config: {}".format(config))


def read_file(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()


def conf():
    return config

