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
import os

class ZDatasetFactCollector(BaseFactCollector):
    name = "zos_dataset"
    _fact_ids = set(["zos_user_datasets"])

    def collect(self, module=None, collected_facts=None):
        datasets = []
        username = os.environ.get('USER')
        rc, out, err = module.run_command("dls {0}.*".format(username.upper()))
        if out and not err:
            for dataset in out.split("\n"):
                datasets.append(dataset)
        datasets = [dataset for dataset in datasets if dataset]
        return {"zos_user_datasets": datasets}
