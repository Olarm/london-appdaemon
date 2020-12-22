import time
import datetime
import hassapi as hass
import datetime

class CoffeeMachine(hass.Hass):
  def initialize(self):
    self.switch = self.args["switch"]
    self.sensor = self.args["sensor"]

    self.listen_state(self.power_on, self.sensor, old="0.0")
    self.listen_state(self.power_off, self.sensor, duration=2, new="0.0")

  def power_on(self, *args, **kwargs):
    self.log("Coffeemaker switched on, startingtimers", log = "main_log")
    self.boil_timer = self.run_in(self.boil_check, delay=3)
    self.off_timer = self.run_in(self.coffee_timer, delay=900)

  def power_off(self, *args, **kwargs):
    self.log("Coffeemaker switched off, stopping timers", log = "main_log")
    try:
      self.cancel_timer(self.off_timer)
    except AttributeError:
      pass
    try:
      self.cancel_timer(self.boil_timer)  
    except AttributeError:
      pass

  def coffee_timer(self, *args, **kwargs):
    power = self.get_state(self.sensor)
    if float(power) > 0:
      self.log("Coffeemaker on for too long, switching off", log = "main_log")
      self.turn_off(self.switch)

  def boil_check(self, *args, **kwargs):
    power = self.get_state(self.sensor)
    if float(power) == 0:
      pass
    elif float(power) < 1000:
      self.log("Coffeemaker started empty, switching off", log = "main_log")
      self.turn_off(self.switch)
    else:
      self.log("Coffeemaker boiling", log = "main_log")
