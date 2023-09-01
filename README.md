# Fishbuster - Core
**Fishbuster Core** is a part of the infrastructure of the free browser extension Fishbuster.
The core, is used to predict the probability for a domain to be malicious. The weights in the `prediction.py` files have
been calculated using machine learning on real-world data.


## Installation

#### Dependencies
This project uses only native python libraries except `Flask` (https://flask-fr.readthedocs.io/), the library for making
the http server and `Redis` (https://redis.io/docs/clients/python/) for a fast database, so the extension doesn't 
trigger too late.
#### Deploy
You can either :
- Run the core for **debugging/testing** with `python app.py`
- Deploy the core for **production** with Apache2

1. Create the directory fishbusterCore
2. Move all files from the repo to a new directory named `app`
3. Create a python virtual environment `python -m venv /path/to/venv`
4. Install the dependencies onto that virtual environment : `source /path/to/venv/bin/activate && pip install Redis flask`
5. Create the `app.wsgi` file for the server in the directory containing `app.py`
``` python
from __future__ import unicode_literals
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, 'path/to/fishbusterCore/app')
from app import app as application
```
6. Create the Apache2 configuration file
```
WSGIPythonHome /path/to/venv
# <VirtualHost *:443> #Optional, if you want to install fishbusterCore as a vhost
WSGIScriptAlias / /path/to/fishbusterCore/app/app.wsgi
# Servername example.com
<Directory /path/to/fishbusterCore/app>
            Options FollowSymLinks
            AllowOverride None
            Require all granted
</Directory>
# </VirtualHost>
```

### BSD 3-clause License

With this project, you are **free** to:

- **Use** - Utilize the software in any context or capacity, including for commercial purposes.
- **Modify** - Alter the source code to fit your needs or specifications.
- **Distribute** - Share the software in both its original or modified form.

**Maintain Original Copyright Notices** 
- **Retain all original copyright notices and disclaimers** if you redistribute the software in source or binary form.
- **Not Misrepresent Endorsement**: Refrain from using the name of this project, its contributors, or associated organizations to endorse or promote products derived from this software without specific prior written permission.

**For the full license text and details, please refer to the LICENSE file in the project root.**


### Contact or support
You can email me at **q78d1s2b@duck.com** for contact, support or pull requests.