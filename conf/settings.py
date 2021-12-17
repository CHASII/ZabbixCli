'''
Author: Chas
LastEditors: Chas
Version: 
Description: 
'''
import logging
import os
import sys

# Log Set
logger = logging.getLogger('zbx')
logger.setLevel(logging.DEBUG)
log_fmt = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s：%(message)s'

# Export Console
rf_handler = logging.StreamHandler(sys.stderr)
rf_handler.setLevel(logging.INFO) 
rf_handler.setFormatter(logging.Formatter(log_fmt))
logger.addHandler(rf_handler)

# Export Logfile
f_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
f_path = os.path.join(f_dir, "logs", "zbx.log")
f_handler = logging.FileHandler(f_path, encoding='utf-8')
f_handler.setLevel(logging.WARNING)
f_handler.setFormatter(logging.Formatter(log_fmt))
logger.addHandler(f_handler)

# Env Set
Zabbix = {
    "api": "http://<your_ip>/api_jsonrpc.php",
    "user": "<your_name>",
    "pass": "<your_pswd>",
    "gwidth": 900,
    "gheight": 200
}
