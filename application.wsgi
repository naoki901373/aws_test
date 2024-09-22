import sys

sys.path.insert(0, '/var/www/wrk')
sys.path.insert(0, '/home/ec2-user/.local/lib/python3.7/site-packages/')
from app import app as application