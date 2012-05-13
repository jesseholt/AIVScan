#!/bin/bash
# hacky way to find the PIDs for gunicorn_django and kill the processes.

kill -9 `ps -e | grep gunicorn_django | awk '{print $1}'`