import os

is_testing = os.getenv('KRAKEN__ENV', '') == 'testing'
