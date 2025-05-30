import logging

from control import data
from helpermodules import compatibility
from modules.common.component_state import InverterState
from modules.common.fault_state import FaultState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store._broker import pub_to_broker
from modules.common.store.ramdisk import files

log = logging.getLogger(__name__)


class InverterValueStoreRamdisk(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.__pv = files.pv[component_num - 1]

    def set(self, inverter_state: InverterState):
        try:
            self.__pv.power.write(int(inverter_state.power))
            self.__pv.energy.write(inverter_state.exported)
            self.__pv.energy_k.write(inverter_state.exported / 1000)
            if inverter_state.currents:
                self.__pv.currents.write(inverter_state.currents)
        except Exception as e:
            raise FaultState.from_exception(e)


class InverterValueStoreBroker(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, inverter_state: InverterState):
        self.state = inverter_state

    def update(self):
        pub_to_broker("openWB/set/pv/" + str(self.num) + "/get/power", self.state.power, 2)
        if self.state.exported is not None:
            pub_to_broker("openWB/set/pv/" + str(self.num) + "/get/exported", self.state.exported, 3)
        else:
            log.debug("Kein gültiger Zählerstand. Wert wird nicht aktualisiert.")
        if self.state.currents:
            pub_to_broker("openWB/set/pv/" + str(self.num) + "/get/currents", self.state.currents, 1)


class PurgeInverterState:
    def __init__(self, delegate: LoggingValueStore) -> None:
        self.delegate = delegate

    def set(self, state: InverterState) -> None:
        self.delegate.set(state)

    def update(self) -> None:
        state = self.filter_peaks(self.delegate.delegate.state)
        state = self.fix_hybrid_values(state)
        self.delegate.set(state)
        self.delegate.update()

    def filter_peaks(self, state: InverterState) -> InverterState:
        inverter = data.data.pv_data[f"pv{self.delegate.delegate.num}"]
        max_ac_out = inverter.data.config.max_ac_out
        if max_ac_out > 0 and state.power > max_ac_out:
            state.power = max_ac_out
        return state

    def fix_hybrid_values(self, state: InverterState) -> InverterState:
        children = data.data.counter_all_data.get_entry_of_element(self.delegate.delegate.num)["children"]
        power = state.power
        exported = state.exported
        imported = state.imported
        if len(children):
            hybrid = []
            for c in children:
                if c.get("type") == "bat":
                    hybrid.append(f'bat{c["id"]}')
                    break
            if len(hybrid):
                for bat in hybrid:
                    bat_get = data.data.bat_data[bat].data.get
                    power -= bat_get.power

                    exported += bat_get.imported - bat_get.exported - imported

            if state.dc_power is not None:
                # Manche Systeme werden auch aus dem Netz geladen, um einen Mindest-SoC zu halten.
                if state.dc_power == 0:
                    power = 0
        state.power = power
        state.exported = exported
        return state


def get_inverter_value_store(component_num: int) -> PurgeInverterState:
    return PurgeInverterState(LoggingValueStore(
        (InverterValueStoreRamdisk if compatibility.is_ramdisk_in_use() else InverterValueStoreBroker)(component_num)
    ))
