# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.facts.collector import BaseFactCollector
import re

class ZIplFactCollector(BaseFactCollector):
    name = "zos_ipl"
    _fact_ids = set(["zos_ipl_info"])

    def collect(self, module=None, collected_facts=None):
        ipl_info = {}
        rc, out, err = module.run_command("opercmd 'd iplinfo'")
        if err:
            return {"zos_ipl_info": ipl_info}
        time_match = re.search(r'^\s+SYSTEM\sIPLED\sAT\s([0-9\.]+)\sON\s([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})$', out, re.MULTILINE)
        time = {}
        if time_match:
            time["time"] = time_match.group(1)
            time["date"] = time_match.group(2)
        ipl_info["last_ipl"] = time
        load_dataset_match = re.search(r'^\s+USED\s([^\s]+)\sIN\s([^\s]+)\sON.*$', out, re.MULTILINE)
        load_dataset = ""
        if load_dataset_match:
            load_dataset = "{0}({1})".format(load_dataset_match.group(2), load_dataset_match.group(1))
        ipl_info["load_dataset"] = load_dataset
        level_share_match = re.search(r'^\s+ARCHLVL\s\=\s([0-9]+)\s+MTLSHARE\s=\s([YN])$', out, re.MULTILINE)
        level_share = {}
        if level_share_match:
            level_share["archlvl"] = level_share_match.group(1)
            level_share["mtlshare"] = level_share_match.group(2)
        ipl_info["level_share"] = level_share
        ieasym_match = re.search(r'^\s+IEASYM\sLIST\s\=\s[\(]?([A-Z0-9,]+)[\)]?$', out, re.MULTILINE)
        ieasym_list = []
        if ieasym_match:
            ieasym_list = ieasym_match.group(1).split(',')
        ipl_info["ieasym_list"] = ieasym_list
        ieasys_match = re.search(r'^\s+IEASYS\sLIST\s\=\s[\(]?([A-Z0-9,]+)[\)]?.*$', out, re.MULTILINE)
        ieasys_list = []
        if ieasys_match:
            ieasys_list = ieasys_match.group(1).split(',')
        ipl_info["ieasys_list"] = ieasys_list
        iodf_device_match = re.search(r'^\s+IODF\sDEVICE:\sORIGINAL\(([A-Z0-9]+)\)\sCURRENT\(([A-Z0-9]+)\)$', out, re.MULTILINE)
        iodf_device = {}
        if iodf_device_match:
            iodf_device["original"] = iodf_device_match.group(1)
            iodf_device["current"] = iodf_device_match.group(2)
        ipl_info["iodf_device"] = iodf_device
        ipl_device_match = re.search(r'^\s+IPL\sDEVICE:\sORIGINAL\(([A-Z0-9]+)\)\sCURRENT\(([A-Z0-9]+)\)\sVOLUME\(([A-Z0-9]+)\)$', out, re.MULTILINE)
        ipl_device = {}
        if ipl_device_match:
            ipl_device["original"] = ipl_device_match.group(1)
            ipl_device["current"] = ipl_device_match.group(2)
        ipl_info["ipl_device"] = ipl_device
        return {"zos_ipl_info": ipl_info}