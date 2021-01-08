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

class ZCpuFactCollector(BaseFactCollector):
    name = "zos_cpu"
    _fact_ids = set(["zos_cpu_info"])

    def collect(self, module=None, collected_facts=None):
        cpu_info = {}
        rc, out, err = module.run_command("opercmd 'd m'")
        if err:
            return {"zos_cpu_info": cpu_info}
        cores_match = re.finditer(r'^\s+([0-9]{4})\s+([^\s]+)\s+([0-9\-]+)\s+((?:[A-Z]+)?)\s+([A-Z0-9]+)\s+([^\s]+)', out, re.MULTILINE)
        cores = []
        for core_match in cores_match:
            core = {}
            core["id"] = core_match.group(1)
            core["status"] = core_match.group(2)
            core["id_range"] = core_match.group(3)
            core["vp"] = core_match.group(4)
            core["iscm"] = core_match.group(5)
            core["cpu_thread_status"] = core_match.group(6)
            cores.append(core)
        cpu_info["cores"] = cores
        core_status_match = re.search(r'^\s+CORE\sSTATUS\:\s(.*)$', out, re.MULTILINE)
        core_status = ""
        if core_status_match:
            core_status = core_status_match.group(1).rstrip()
        cpu_info["core_status"] = core_status
        channel_paths_match = re.finditer(r'^\s+[0-9A-F]\s+([\s\.\+\@\-]+)$', out, re.MULTILINE)
        channel_paths = []
        if channel_paths_match:
            for channel_path_match in channel_paths_match:
                channel_path = channel_path_match.group(1).split(" ")
                channel_paths.append(channel_path)
        cpu_info["channel_path_status"] = channel_paths
        return {"zos_cpu_info": cpu_info}
