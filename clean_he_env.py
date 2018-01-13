#!/usr/bin/env python2.7
__author__ = "yzhao@redhat.com"

import re
import os
import time
import logging
import commands
import subprocess

try:
        logging.warning("-=== Destroy hosted-engine VM ===-")
        subprocess.call("hosted-engine  --vm-poweroff", shell=True)
        time.sleep(3)

        logging.warning("-=== Destroy the VMs ===-")
        (value, host) = commands.getstatusoutput("vdsm-client Host getVMList")
        pattern = re.compile('"(.*)"')
        hostlist = pattern.findall(host)
        for i in hostlist:
            os.system("vdsm-client VM destroy vmID=%s" % i)

        time.sleep(5)

        logging.warning("-=== Stop HA services ===-")
        subprocess.call("systemctl stop ovirt-ha-agent ovirt-ha-broker", shell=True)
        #os.system("systemctl stop ovirt-ha-agent ovirt-ha-broker vdsmd")
        time.sleep(5)

        logging.warning("-=== Shutdown sanlock ===-")
        subprocess.call("sanlock client shutdown -f 1", shell=True)

        logging.warning("-=== Disconnecting the hosted-engine storage domain ===-")
        subprocess.call("hosted-engine --disconnect-storage", shell=True)

        logging.warning("-=== Re-configure VDSM networks ===-")
        subprocess.call("vdsm-tool restore-nets", shell=True)

        logging.warning("-=== Stop other services ===-")
        subprocess.call("systemctl stop vdsmd supervdsmd libvirtd momd sanlock", shell=True)

        logging.warning("-=== Re-configure external daemons ===-")
        subprocess.call("vdsm-tool remove-config", shell=True)

except Exception as e:
    logging.error(e)

finally:
        logging.warning("-=== Removing configuration files ===-")
        subprocess.call("rm -rf /etc/init/libvirtd.conf \
                        /etc/libvirt/nwfilter/vdsm-no-mac-spoofing.xml \
                        /etc/ovirt-hosted-engine/answers.conf \
                        /etc/ovirt-hosted-engine/hosted-engine.conf /etc/vdsm/vdsm.conf \
                        /etc/pki/vdsm/*/*.pem /etc/pki/CA/cacert.pem /etc/pki/libvirt/*.pem \
                        /etc/pki/libvirt/private/*.pem /etc/pki/ovirt-vmconsole/*.pem \
                        /var/cache/libvirt/* /var/run/ovirt-hosted-engine-ha/*", shell=True)

        logging.warning("-=== Finish cleaning the SHE ENV ===-")

