# -*- coding: utf-8 -*-

'''*
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*'''

import xbmc
import time

from commoncore.kodi import addon, logger

enable_updates = addon.get_setting('enable_updates') == 'true'

class UpdateService():

    last_run = False
    # every 24 hours
    update_interval = 86400

    def update(self):
        if enable_updates:
            if not self.last_run or time.time() - self.last_run > self.update_interval:
                self.last_run = time.time()
                plugin_url = addon.build_plugin_url({
                    "mode": "update_addons",
                    "quiet": "quiet"
                }, addon.get_id())
                addon.execute_url(plugin_url)

    def start(self):

        enable_updates
        class Monitor(xbmc.Monitor):
            def onSettingsChanged(self):
                global enable_updates
                enable_updates = addon.get_setting('enable_updates') == 'true'
        monitor = Monitor()
        logger.log("Service Starting...")

        while not monitor.abortRequested():
            if monitor.waitForAbort(10):
                break
            self.update()

        self.shutdown()


    def shutdown(self):
        logger.log("Service Stopping...")


if __name__ == '__main__':
    server = UpdateService()
    server.start()
