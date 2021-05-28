__author__ = 'JG'

import os
import argparse
from config import environment as env
env.suite['workspace'] = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument('--log_level', type=str, help='Set log level for execution', default='DEBUG')
args = parser.parse_args()

env.suite['log_level'] = args.log_level

from lib import utility as util
log = util.Log()

ipv4_address = util.Network().get_ipv4()
log.info(f'Prodapt test service is running on {ipv4_address}')

from webapp import api
app = api()
app.run(host=ipv4_address, port=5000, debug=True, threaded=True)
