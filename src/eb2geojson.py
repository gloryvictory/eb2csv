#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   Author  :   Vyacheslav Zamaraev
#   Date    :   21.09.2023
#   Desc    :   eb 2 csv

import os
from datetime import datetime
import logging
import cfg

# import requests
# from bs4 import BeautifulSoup
# import random
# from time import sleep


def Main():
    print('Start!!!')
    time1 = datetime.now()
    print(time1)

    for handler in logging.root.handlers[:]:  # Remove all handlers associated with the root logger object.
        logging.root.removeHandler(handler)
    logging.basicConfig(filename=cfg.FILE_LOG, format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG,
                        filemode='w')  #
    logging.info(cfg.FILE_LOG)
    logging.info(time1)





    time2 = datetime.now()
    logging.info(time2)
    print(time2)
    print(time2 - time1)
    logging.info(str(time2 - time1))
    print('DONE !!!!')


if __name__ == '__main__':
    Main()
