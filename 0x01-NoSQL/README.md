# NoSQL Databases with MongoDB and Python
This project gives a deep understanding of NoSQL databases, focusing on MongoDB and its integration with python

## Requirements
+ All tasks are run on Ubuntu 18.04 LTS using MongoDB (version 4.2)
+ All scripts are written in Python 3.7 and use PyMongo (version 3.10).
+ Python scripts comply with pycodestyle (version 2.5).

## Setup Instructions

### Installing MongoDB (version 4.2) on Ubuntu 18.04:

1. Import the public key:
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
```

2. Add MongoDB repository:
```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
```

3. update your package list and install MongoDB:
```
sudo apt-get update
sudo apt-get install -y mongodb-org
```

4. Start the MongoDB service:
```
sudo service mongod start
```

5. Verify MongoDB installation:
```
mongo --version
```

### Installing PyMongo:

+ Install using pip:
```
pip3 install pymongo
```

+ check PyMongo version:
```
python3
>>> import pymongo
>>> pymongo.__version__
 '3.10.1'
```

## Important Notes:
+ If you encounter an error regarding the data directory **(/data/db not found)**, create the directory using:
```
sudo mkdir -p /data/db
```

+ If **/etc/init.d/mongod** is missing, refer to the official documentation for addiitional setup instructions.
