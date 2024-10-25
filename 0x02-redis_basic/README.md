# Redis Basic

## Project Overview
This peoject demonstrates:
- Basic Redis commands and operations
- Redis python client setup and usage
- Using Redis as a simple caching mechanism

## Requirements
- **Ubuntu 18.04 LTS** using python 3.7.
- **pycodestyle(version 2.5.)**

## Setup
1. Install Redis:
```
sudo apt-get -y install redis-server
```

2. Install Redis Python client:
```
pip3 install redis
```

3. Configure Redis to bind to localhost:
```
sudo sed -i "s/bind .*/bind 127.0.0.1/g" /etc/redis/redis.conf
```

## Running Redis in a Container
By default, the Redis server is stopped. When starting a container, you should start Redis with:
```
service redis-server start
```
