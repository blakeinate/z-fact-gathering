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
import os

class ZAliasFactCollector(BaseFactCollector):
    name = "zos_alias"
    _fact_ids = set(["zos_user_alias"])


    def collect(self, module=None, collected_facts=None):
        alias = ""
        username = os.environ.get('USER')
        rc, out, err = module.run_command('echo " LISTCAT ENTRIES({0})" | mvscmdauth --pgm=idcams --sysin=stdin --sysprint=*'.format(username.upper()), use_unsafe_shell=True)
        if err:
            return {"zos_user_alias": alias}
        alias_match = re.search(r'ALIAS\s-*\s[A-Z0-9]+\n\s+IN-CAT\s-*\s(.*)$', out, re.MULTILINE)
        if alias_match:
            alias = alias_match.group(1)
        return {"zos_user_alias": alias}