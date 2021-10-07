#!/bin/bash

/etc/init.d/redis-server start
/etc/init.d/nginx start
/etc/init.d/supervisor start

tail -F /home/python/cloudpanel/django.log