## Start chrony
sudo $(brew --prefix chrony)/sbin/chronyd -d -f $(brew --prefix)/etc/chrony.conf

## Validate it is running
ps aux | grep chronyd
chronyc sources

## Test Connection
sntp 127.0.0.1
python tests/local_test.py