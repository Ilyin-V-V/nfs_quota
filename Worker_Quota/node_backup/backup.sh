#!/bin/bash
date=$(date '+%Y-%m-%d %H:%M:%S'); dir=$(date '+%Y%m%d%H%M');
host_backup=//host.domain.ru/nfs; mount_backup=/home/backup/;
log=/var/log/messages;

function clear(){
 local index=0; for variable in `ls -lt $mount_backup | awk '{print $NF}'`; do
   if [ "$index" -gt "0" ]; then if [ "$index" -gt "7" ]; then
     echo $date "Clear folder" $variable >> $log; echo $date "Clear folder" $variable;
     /usr/bin/rm -rf $mount_backup$variable; fi; fi; index=$(($index + 1));done
}

mount=$(/usr/bin/mount -t cifs -o user=guest,pass= $host_backup $mount_backup);
df=$(/usr/bin/df | /usr/bin/grep backup); if [ "$df" ]; then
 echo $date "Mount backup start" $mount_backup >> $log; clear;
 /usr/bin/mkdir $mount_backup$dir-$HOSTNAME;
 /usr/bin/cp -a /boot $mount_backup$dir-$HOSTNAME/boot;
 /usr/sbin/vgcfgbackup -f $mount_backup$dir-$HOSTNAME/lvm;
 /usr/sbin/lvcreate -s -n backup -L10G /dev/mapper/vg_main-lv_root;
 /usr/sbin/partclone.ext4 -c -s /dev/mapper/vg_main-backup -o $mount_backup$dir-$HOSTNAME/vg-root.img;
 /usr/sbin/lvremove -y /dev/mapper/vg_main-backup;/usr/bin/umount $mount_backup;
 echo $date "Mount backup end" $mount_backup >> $log; fi
if [ -z "$df" ]; then echo $date "Mount problem " $mount_backup $mount $df >> $log; fi

