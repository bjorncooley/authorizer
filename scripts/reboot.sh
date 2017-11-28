# simple reboot for ubuntu 16.04 box with gunicorn and nginx as proxy server
systemctl restart gunicorn.socket
systemctl restart nginx.service
