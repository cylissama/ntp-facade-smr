# Testing

This test was done using a Docker container running an image of: https://hub.docker.com/r/cturra/ntp

Then we run our test script to ensure the container is running, and a connection is getting through the container to the host device's network.

## Start chrony
sudo $(brew --prefix chrony)/sbin/chronyd -d -f $(brew --prefix)/etc/chrony.conf

## Validate it is running
ps aux | grep chronyd
chronyc sources

## Test Connection
sntp 127.0.0.1
python tests/local_test.py
