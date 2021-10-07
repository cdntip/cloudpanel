#!/bin/bash

/etc/init.d/redis-server start
/etc/init.d/nginx start
/etc/init.d/supervisor start