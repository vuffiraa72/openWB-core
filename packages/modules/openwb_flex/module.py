from typing import List

try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from . import evu_kit
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    import evu_kit


class Module():
    def __init__(self, device: dict) -> None:
        try:
            self.data = {}
            self.data["config"] = device
            self.data["components"] = {}
            ip_address = self.data["config"]["configuration"]["ip_address"]
            port = self.data["config"]["configuration"]["port"]
            self.client = connect_tcp.ConnectTcp(self.data["config"]["name"], self.data["config"]["id"], ip_address, port)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+device["name"])

    def add_component(self, component_config: dict) -> None:
        try:
            if component_config["type"] == "counter":
                self.data["components"]["component"+str(component_config["id"])] = evu_kit.EvuKitFlex(self.data["config"]["id"], component_config, self.client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def read(self):
        try:
            if len(self.data["components"]) > 0:
                self.data["components"]["component0"].read()
            else:
                log.MainLogger().warning(self.data["config"]["name"]+": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden.")
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])


def read_legacy(argv: List):
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        component_type = str(argv[1])
        version = int(argv[2])
        ip_address = str(argv[3])
        port = int(argv[4])
        id = int(argv[5])

        device0 = {"name": "OpenWB-Kit", "type": "openwb_flex", "id": 0, "configuration": {"ip_address": ip_address, "port": port},
                   "components": {"component0": {"name": "EVU-Kit flex", "type": component_type, "id": 0, "configuration": {"version": version, "id": id}}}}
        mod = Module(device0)

        log.MainLogger().debug('openWB Version: ' + str(version))
        log.MainLogger().debug('Counter-Module EVU-Kit IP-Adresse: ' + str(ip_address))
        log.MainLogger().debug('Counter-Module EVU-Kit Port: ' + str(port))
        log.MainLogger().debug('Counter-Module EVU-Kit ID: ' + str(id))

        mod.read()
    except Exception as e:
        log.MainLogger().exception("Fehler im Modul openwb_flex")


if __name__ == "__main__":
    read_legacy(sys.argv)