#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "usage: ./add_user.sh username"
    exit 1
fi

echo "Adding user $1"
while true; do
    read -s -p "Enter new password: " password
    echo
    read -s -p "Enter new password(again): " password2
    echo
    [ "$password" = "$password2" ] && break
    echo "Please try again"
done

rediscli='~/redis/redis-6.2.4/src/redis-cli'
pass_hash=`python -c "from werkzeug.security import generate_password_hash as h; print(h('$password'))"`
eval "$rediscli set u:$1:pwd $pass_hash"
