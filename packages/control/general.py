"""Allgemeine Einstellungen
"""
from dataclasses import dataclass, field
import logging
import random
from typing import List, Optional

from control import data
from control.bat_all import BatConsiderationMode
from helpermodules import timecheck

log = logging.getLogger(__name__)


def control_range_factory() -> List:
    return [0, 230]


@dataclass
class PvCharging:
    bat_power_reserve: int = field(default=2000, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_reserve"})
    bat_power_reserve_active: bool = field(default=False, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_reserve_active"})
    control_range: List = field(default_factory=control_range_factory, metadata={
        "topic": "chargemode_config/pv_charging/control_range"})
    feed_in_yield: int = field(default=15000, metadata={
        "topic": "chargemode_config/pv_charging/feed_in_yield"})
    phase_switch_delay: int = field(default=7, metadata={
        "topic": "chargemode_config/pv_charging/phase_switch_delay"})
    bat_power_discharge: int = field(default=1500, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_discharge"})
    bat_power_discharge_active: bool = field(default=False, metadata={
        "topic": "chargemode_config/pv_charging/bat_power_discharge_active"})
    min_bat_soc: int = field(default=50, metadata={
        "topic": "chargemode_config/pv_charging/min_bat_soc"})
    bat_mode: BatConsiderationMode = field(default=BatConsiderationMode.EV_MODE.value, metadata={
        "topic": "chargemode_config/pv_charging/bat_mode"})
    switch_off_delay: int = field(default=60, metadata={
                                  "topic": "chargemode_config/pv_charging/switch_off_delay"})
    switch_off_threshold: int = field(default=0, metadata={
        "topic": "chargemode_config/pv_charging/switch_off_threshold"})
    switch_on_delay: int = field(default=30, metadata={
        "topic": "chargemode_config/pv_charging/switch_on_delay"})
    switch_on_threshold: int = field(default=1500, metadata={
        "topic": "chargemode_config/pv_charging/switch_on_threshold"})


def pv_charging_factory() -> PvCharging:
    return PvCharging()


@dataclass
class ChargemodeConfig:
    phase_switch_delay: int = field(default=5, metadata={
        "topic": "chargemode_config/phase_switch_delay"})
    pv_charging: PvCharging = field(default_factory=pv_charging_factory)
    retry_failed_phase_switches: bool = field(
        default=False,
        metadata={"topic": "chargemode_config/retry_failed_phase_switches"})
    unbalanced_load_limit: int = field(
        default=18, metadata={"topic": "chargemode_config/unbalanced_load_limit"})
    unbalanced_load: bool = field(default=False, metadata={
                                  "topic": "chargemode_config/unbalanced_load"})


def chargemode_config_factory() -> ChargemodeConfig:
    return ChargemodeConfig()


@dataclass
class Prices:
    bat: float = field(default=0.0002, metadata={"topic": "prices/bat"})
    cp: float = field(default=0, metadata={"topic": "prices/cp"})
    grid: float = field(default=0.0003, metadata={"topic": "prices/grid"})
    pv: float = field(default=0.00015, metadata={"topic": "prices/pv"})


def prices_factory() -> Prices:
    return Prices()


@dataclass
class GeneralData:
    chargemode_config: ChargemodeConfig = field(default_factory=chargemode_config_factory)
    control_interval: int = field(default=10, metadata={"topic": "control_interval"})
    extern_display_mode: str = field(default="primary", metadata={
                                     "topic": "extern_display_mode"})
    extern: bool = field(default=False, metadata={"topic": "extern"})
    external_buttons_hw: bool = field(
        default=False, metadata={"topic": "external_buttons_hw"})
    grid_protection_active: bool = field(
        default=False, metadata={"topic": "grid_protection_active"})
    grid_protection_configured: bool = field(
        default=True, metadata={"topic": "grid_protection_configured"})
    grid_protection_random_stop: int = field(
        default=0, metadata={"topic": "grid_protection_random_stop"})
    grid_protection_timestamp: Optional[float] = field(
        default=None, metadata={"topic": "grid_protection_timestamp"})
    http_api: bool = field(
        default=False, metadata={"topic": "http_api"})
    mqtt_bridge: bool = False
    prices: Prices = field(default_factory=prices_factory)
    range_unit: str = "km"


class General:
    """
    """

    def __init__(self):
        self.data: GeneralData = GeneralData()

    def grid_protection(self):
        """ Wenn der Netzschutz konfiguriert ist, wird geprüft, ob die Frequenz außerhalb des Normalbereichs liegt
        und dann der Netzschutz aktiviert. Bei der Ermittlung des benötigten Stroms im EV-Modul wird geprüft, ob
        der Netzschutz aktiv ist und dann die Ladung gestoppt.
        """
        try:
            evu_counter = data.data.counter_all_data.get_evu_counter_str()
            if self.data.grid_protection_configured:
                frequency = data.data.counter_data[evu_counter].data.get.frequency * 100
                grid_protection_active = self.data.grid_protection_active
                if not grid_protection_active:
                    if 4500 < frequency < 4920:
                        self.data.grid_protection_random_stop = random.randint(
                            1, 90)
                        self.data.grid_protection_timestamp = timecheck.create_timestamp(
                        )
                        self.data.grid_protection_active = True
                        log.info("Netzschutz aktiv! Frequenz: " +
                                 str(data.data.counter_data[evu_counter].data.get.frequency)+"Hz")
                    if 5180 < frequency < 5300:
                        self.data.grid_protection_random_stop = 0
                        self.data.grid_protection_timestamp = None
                        self.data.grid_protection_active = True
                        log.info("Netzschutz aktiv! Frequenz: " +
                                 str(data.data.counter_data[evu_counter].data.get.frequency)+"Hz")
                else:
                    if 4962 < frequency < 5100:
                        self.data.grid_protection_active = False
                        log.info("Netzfrequenz wieder im normalen Bereich. Frequenz: " +
                                 str(data.data.counter_data[evu_counter].data.get.frequency)+"Hz")
                        self.data.grid_protection_timestamp = None
                        self.data.grid_protection_random_stop = 0
        except Exception:
            log.exception("Fehler im General-Modul")
