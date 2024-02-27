#!/bin/sh

#capacity = BLOCKS (each block 512 byte)
#apt-get install thttpd ash
#chmod +s /bin/dd /sbin/hdparm /sbin/fdisk
#adduser www-data disk floppy and restart thttpd
#modprobe /lib/modules/`uname -k`/fs/ filesystems you need .o

#dd if=/dev/hda bs=8192 | ssh user@otherbox 'dd of=/dev/hdwhatever bs=8192'

title="ubercopy"
hdparameter="-c1 -d1"

#generate a report about copy
#locking(start/finish copy)
#size destination=>source
#don't copy mounted media(or ro only)
#notification(mail/audio)/check status
#file: set name
#ERROR no media found
#network copy?

echo -e "Content-type: text/html\n\n"

if [ $QUERY_STRING ]; then
a=`echo $QUERY_STRING |perl -e '$s=<STDIN>; $s=~s/%([0-9a-f][0-9a-f])/pack("C",hex($1))/egi; print $s;'` #|sed "s/\&/;/g"
set -- `echo $a |awk 'BEGIN {FS="&"}{print $0}'|sed "s/+/\ /g" |sed "s,\&,\ ,g"`

if [ ! "x$1" = "x" ]; then
    for i in "$1 $2 $3 $4"; do
        #eval echo \$i = \$$i
        export $i
        done
    fi
fi
			
echo "<html>"
echo "<title>$title</title>"
#echo "<style type="text/css"><!--"
#ehco "a:link { text-decoration: none }"
#echo "a:active { text-decoration: none }"
#echo "a:visited { text-decoration: none }"
#echo "--></style>"
echo "<body text=#000000 link=#000000 vlink=#000000 alink=#000000 bgcolor=#ffffff>"
echo "<font face=\"lucida, verdana, helvetica\" size=2>"
echo "<pre>"
echo -n "<h1>ubercopy</h1><p>"

echo -n "<a href=index.cgi>main</a> "
echo -n "<a href=index.cgi?help=list>help</a> "
echo -n "<a href=index.cgi?fdisk=list>fdisk -l</a> "
echo -n "<a href=index.cgi?dmesg=list>dmesg</a> "
echo -n "<a href=index.cgi?hdparm=list>hdparm</a> "
echo -n "<a href=index.cgi?listimg=list>list *.img</a> "
echo -n "<a href=index.cgi?fs=list>filesystems</a> "
echo "<br>"

if [ ! "x$fdisk" = "x" ]; then
    /sbin/fdisk -l
    exit
fi
if [ ! "x$dmesg" = "x" ]; then
    dmesg
    exit
fi
if [ ! "x$help" = "x" ]; then
    #help? man dd
    echo "HELP! HELP!"
    exit
fi
if [ ! "x$hdparm" = "x" ]; then
    for a in a b c d e f g h; do
	/sbin/hdparm $hdparameter /dev/hd${a}
    done
    exit
fi
if [ ! "x$listimg" = "x" ]; then
    for a in *.img; do
	printf "<a href=$a>"
        ls -la $a
	printf "</a>"
    done
    exit
fi
if [ ! "x$fs" = "x" ]; then
    cat /proc/filesystems |grep -v "^nodev"
    exit
fi

echo "<b>Information</b>"
echo "<table><tr><td valign=top>"
for a in hda hdb hdc hdd hde hdf hdg hdh; do
    if [ -d /proc/ide/$a ]; then
	echo "<font face=\"lucida, verdana, helvetica\" size=2>"
	if [ -f /proc/ide/$a/capacity ]; then siz=`cat /proc/ide/$a/capacity`; else siz=0; fi
        echo "$a (`echo $siz / 2000 |bc` mb)<br>"
        for b in model media cache capacity geometry; do #settings
            if [ -f /proc/ide/$a/$b ]; then
                echo $b `cat /proc/ide/$a/$b`"<br>"
	    else
		echo "<br>"
            fi
        done
	echo "</td><td valign=top>"
    fi
done
echo "</td></tr></table>"

echo "<b>Please select source and destination carefully and confirm copy</b>"
printf "<table><tr><form action=\"index.cgi\" method=get>"
printf "<td><select name=\"source\" size=8>\n"
cat devices |while read a; do
    b=`echo $a|sed "s/<option>//g"`
    head $b &>/dev/null && echo $a
done
for a in *.img; do
    if [ -f $a ]; then 
	echo "<option>$a"
    fi
done
printf "</select></td>"

printf "<td><select name=\"destination\" size=8>\n"
cat devices |while read a; do
    b=`echo $a|sed "s/<option>//g"`
    head $b &>/dev/null && echo $a
done
if [ ! -f file.img ]; then printf "<option>file.img"; fi
printf "</select></td>"
printf "<td valign=bottom><input type=submit border=0 value=\"copy\"></td>"
printf "</form></tr></table><br>"

if [ ! "x$source" = "x" ]; then
    if [ ! "x$destination" = "x" ]; then
	echo
	#mount |grep /dev/hda && echo can not copy mounted media
	if [ "x$source" = "x$destination" ]; then
	    echo "<b>ERROR</b> destination ($destination) may not be the same as source ($source)"
        else
	    echo Please wait "dd if=$source of=$destination bs=1024k"
	    date
	    time dd if=$source of=$destination bs=1024k
	    /bin/sync
	    date
	    #hdparm -Y /dev/hda..h
	fi
    fi
fi

echo "</html>"
