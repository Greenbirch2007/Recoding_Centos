do_setup()
{
vim /home/rdo/packstack-answers-20190118-045535.conf
CONFIG_SAHARA_INSTALL=y
CONFIG_CINDER_VOLUMES_CREATE=n
yum install -y epel-release.noarch
# # cat teamviewer.repo 
# [teamviewer]
# name=TeamViewer - $basearch
# baseurl=http://linux.teamviewer.com/yum/stable/main/binary-$basearch/
# gpgkey=http://linux.teamviewer.com/pubkey/TeamViewer2017.asc
# gpgcheck=1
# enabled=1
# type=rpm-md
# failovermethod=priority
yum install -y teamviewer

# # cat /etc/xdg/autostart/teamviewer.desktop
# [Desktop Entry]
# Type=Application
# Name=TeamviewerRestart
# Exec=/usr/bin/teamviewer daemon restart
# Terminal=false
# X-GNOME-Autostart-enabled=true


sudo systemctl disable firewalld
sudo systemctl stop firewalld
sudo systemctl disable NetworkManager
sudo systemctl stop NetworkManager
sudo systemctl enable network
sudo systemctl start network

vim /etc/fstab 
umount /cinder-volumes
pvcreate /dev/sda4
vgcreate cinder-volumes /dev/sda4

sudo yum install -y centos-release-openstack-stein
yum-config-manager --enable openstack-stein
sudo yum update -y
sudo yum install -y openstack-packstack

vim /usr/share/openstack-dashboard/openstack_dashboard/static/dashboard/img
vim /usr/share/openstack-dashboard/openstack_dashboard/themes/material/templates/material
vim /usr/share/openstack-dashboard/openstack_dashboard/settings.py
SITE_BRANDING = 'Hua Wei Tri-Support'
systemctl restart httpd
vim /etc/nova/nova.conf 
  #vncserver_proxyclient_address=hwts-cloud.www.tendawifi.com
  vncserver_proxyclient_address=192.168.1.133
  block_device_allocate_retries=300
systemctl restart openstack-nova-api.service openstack-nova-compute.service openstack-nova-conductor.service openstack-nova-consoleauth.service openstack-nova-scheduler.service
check cirros size and type

-A INPUT -s 192.168.1.113/32 -p tcp -m multiport --dports 6200,6201,6202,873 -m comment --comment "001 swift storage and rsync incoming swift_storage_and_rsync_192.168.1.113" -j ACCEPT
-A INPUT -s 192.168.1.133/32 -p tcp -m multiport --dports 6200,6201,6202,873 -m comment --comment "001 swift storage and rsync incoming swift_storage_and_rsync_192.168.1.133" -j ACCEPT

yum install ntpd
}
