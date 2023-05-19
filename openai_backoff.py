import time
import asyncio
from openai.error import RateLimitError


class RateLimitError():
  def __init__(self):
    super(RateLimitError, self).__init__("Max delays reached. Rate limit exceeded.")

class ExponentialBackoff:
  def __init__(self, initial_delay=2, max_tries=5, backoff_factor=2.0, max_delay=None,
               async_mode=False):
    self.initial_delay = initial_delay
    self.max_tries = max_tries
    self.backoff_factor = backoff_factor
    self.max_delay = max_delay
    self.current_delay = initial_delay
    self.delay_count = 0
    self.async_mode = async_mode

  def reset(self):
    self.current_delay = self.initial_delay
    self.delay_count = 0

  def delay(self):
    self.delay_count += 1
    if self.delay_count > self.max_tries:
      raise RateLimitError()
    time.sleep(self.current_delay)
    self.current_delay = self.current_delay*self.backoff_factor
    if not self.max_delay is None:
      self.current_delay = min(self.current_delay, self.max_delay)

  async def async_delay(self):
    self.delay_count += 1
    if self.delay_count > self.max_tries:
      raise RateLimitError()
    if self.asych_mode:
      await asyncio.sleep(self.current_delay)
    else:
      time.sleep(self.current_delay)
    self.current_delay = self.current_delay*self.backoff_factor
    if not self.max_delay is None:
      self.current_delay = min(self.current_delay, self.max_delay)