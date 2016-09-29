#! /bin/sh
# /etc/init.d/blah
#

cd /home/pi/github/UtilityMon
sudo chmod 777 /tmp/copyofstream.txt

sudo pkill -9 -f rtl
echo "$(date) - Checking for utility-json running..."
if pgrep "python" > /dev/null
then
 ps -ef | grep utility-json.py | grep -v grep | awk '{print $2}' | xargs kill
fi

echo "Checking for rtl_tcp..."
if pgrep "rtl_tcp" > /dev/null
then

 echo "Killing rtl_tcp..."
 ps -ef | grep rtl_tcp | grep -v grep | awk '{print $2}' | xargs kill
fi

sleep 1

if pgrep "rtl_tcp" > /dev/null
then
 echo "Killing rtl_tcp..."
 ps -ef | grep rtl_tcp | grep -v grep | awk '{print $2}' | xargs kill
fi

sleep 1

if pgrep "rtl_tcp" > /dev/null
then
 echo "Killing rtl_tcp..."
 ps -ef | grep rtl_tcp | grep -v grep | awk '{print $2}' | xargs kill
fi

echo "Checking for rtlamr..."
if pgrep "rtlamr"
then
 sudo killall rtlamr
 sleep 2
fi

if pgrep "rtlamr"
then
 ps -ef | grep rtlamr | grep -v grep | awk '{print $2}' | xargs kill
 sleep 2
fi

if pgrep "rtlamr"
then
 ps -ef | grep rtlamr | grep -v grep | awk '{print $2}' | xargs kill
 sleep 2
fi

if pgrep "rtlamr"
then
 ps -ef | grep rtlamr | grep -v grep | awk '{print $2}' | xargs kill
 sleep 2
fi

sleep 15
python /home/pi/github/UtilityMon/utility-json.py &
