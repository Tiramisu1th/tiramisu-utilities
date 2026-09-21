# AdCom Train timer Logic:
# There are 2 important time stamps: When train arrives, and when train is actually handled
# Let k be the time until first train arrives
# Subsequent trains arrive 1.4k seconds after handling the previous train
# There is also a global timer of 7200 seconds
# Global timer starts when first train is handled
# If a train is handled after global timer expires, reset subsequent train arrival time to 210 seconds
import tkinter as tk
import asyncio
import threading
from desktop_notifier import DesktopNotifier, Button, DEFAULT_SOUND

# Configuration
GLOBAL_TIMER:int = 7200 # 2 hours in seconds
TRAIN_INTERVAL_SECONDS:list[int] = [ 210 , 225 , 309 , 426 , 590 , 820 , 1142 , 1592 , 2222 ] # k1=k0; k_n+1 = 1.4k_n; k+=15
MAX_TRAIN_INDEX:int = len(TRAIN_INTERVAL_SECONDS) - 1

# helper function to format seconds into H:MM:SS or MM:SS
def format_seconds(s: int) -> str:
	if s < 0:
		s = 0
	h = s // 3600
	m = (s % 3600) // 60
	sec = s % 60
	if h:
		return f"{h:d}:{m:02d}:{sec:02d}"
	return f"{m:02d}:{sec:02d}"


class AdComTrainTimer(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("AdCom Train Timer")
		self.train_intervals = TRAIN_INTERVAL_SECONDS
		self.global_timer = GLOBAL_TIMER
		self.current_train_index = 0
		self.time_until_next = self.train_intervals[self.current_train_index]
		self.train_running = False
		self.global_running = False
		self.notified = False
		self.arrived = False
		# start a persistent asyncio loop on a background thread so notifier callbacks
		# and send coroutines run on a stable loop (avoids closed-loop errors)
		self._async_loop = asyncio.new_event_loop()
		self._loop_thread = threading.Thread(target=self._run_async_loop, daemon=True)
		self._loop_thread.start()
		# create notifier on that loop to bind internal callbacks to the running loop
		fut = asyncio.run_coroutine_threadsafe(self._create_notifier(), self._async_loop)
		self.notifier = fut.result(timeout=3)
		self._build_ui()
  
	def _build_ui(self):
		# GUI Logic:
		# Display global timer and time until next train arrives
		# Update GUI every second to reflect current timers
		# Provide a up-and-down arrow button to manually adjust self.current_train_index (>=0 and <= MAX_TRAIN_INDEX)
		# Also provides a button to start and stop the train timer
		# Provides a seperate timer that pauses the global timer and then resets the global timer to 7200 seconds when clicked
		# Lastly, provide a caliberation start/stop button that allows user to measure the time between 2 trains to arrive, and set the index to highest possible interval
		# For example, if caliberation timer measures 576 seconds, set index to 4 (805 seconds)
		# When calibration stops, start both train timer and global timer immediately
		self.columnconfigure(0, weight=1)
		frm = tk.Frame(self)
		frm.grid(padx=10, pady=10, sticky="nsew")

		# Global timer display
		self.global_label = tk.Label(frm, text="Global timer:", font=("TKDefaultFont", 14))
		self.global_label.grid(row=0, column=0, sticky="w")
		self.global_time_var = tk.StringVar(value=format_seconds(self.global_timer))
		self.global_time = tk.Label(frm, textvariable=self.global_time_var, font=("TKDefaultFont", 18))
		self.global_time.grid(row=0, column=1, sticky="e")

		# Next train display
		self.next_label = tk.Label(frm, text="Next train in:", font=("TKDefaultFont", 14))
		self.next_label.grid(row=1, column=0, sticky="w")
		self.next_time_var = tk.StringVar(value=format_seconds(self.time_until_next))
		self.next_time = tk.Label(frm, textvariable=self.next_time_var, font=("TKDefaultFont", 18))
		self.next_time.grid(row=1, column=1, sticky="e")

		# Train index controls
		idxfrm = tk.Frame(frm)
		idxfrm.grid(row=2, column=0, columnspan=2, pady=(8,0))
		self.idx_var = tk.StringVar(value=str(self.current_train_index))
		self.idx_label = tk.Label(idxfrm, text="Train index:")
		self.idx_label.pack(side="left")
		self.idx_display = tk.Label(idxfrm, textvariable=self.idx_var, width=3)
		self.idx_display.pack(side="left")
		btn_up = tk.Button(idxfrm, text="▲", command=self._inc_index, width=3)
		btn_up.pack(side="left", padx=4)
		btn_dn = tk.Button(idxfrm, text="▼", command=self._dec_index, width=3)
		btn_dn.pack(side="left")

		# Control buttons
		ctlfrm = tk.Frame(frm)
		ctlfrm.grid(row=3, column=0, columnspan=2, pady=(12,0))
		self.start_btn = tk.Button(ctlfrm, text="Start", width=10, command=self._toggle_start)
		self.start_btn.pack(side="left", padx=4)
		self.handle_btn = tk.Button(ctlfrm, text="Mark Handled", width=12, command=self._mark_handled)
		self.handle_btn.pack(side="left", padx=4)
		self.reset_global_btn = tk.Button(ctlfrm, text="Reset Global", width=12, command=self._reset_global)
		self.reset_global_btn.pack(side="left", padx=4)

		# Calibration controls
		calfrm = tk.Frame(frm)
		calfrm.grid(row=4, column=0, columnspan=2, pady=(12,0))
		self.cal_running = False
		self.cal_time = 0
		self.cal_var = tk.StringVar(value=format_seconds(self.cal_time))
		self.cal_label = tk.Label(calfrm, text="Cal Timer:")
		self.cal_label.pack(side="left")
		self.cal_display = tk.Label(calfrm, textvariable=self.cal_var, width=8)
		self.cal_display.pack(side="left")
		self.cal_start_btn = tk.Button(calfrm, text="Start Cal", command=self._toggle_cal)
		self.cal_start_btn.pack(side="left", padx=6)
		self.cal_mark_btn = tk.Button(calfrm, text="Mark Calibrated", command=self._mark_calibrated)
		self.cal_mark_btn.pack(side="left")

		# Status
		self.status_var = tk.StringVar(value="Idle")
		self.status = tk.Label(frm, textvariable=self.status_var, anchor="w")
		self.status.grid(row=5, column=0, columnspan=2, sticky="we", pady=(8,0))

		# Start update loop
		self._update_loop()

	async def _desktop_notification(self):
		train_index: int = self.current_train_index
		global_timer_display: str = format_seconds(self.global_timer)
		# Build an action that marks the train handled when notification button clicked.
		# Use self.after to ensure the handler runs on the Tk main thread.
		# IMPORTANT: don't call `self.after` here — wrap it in a lambda so the call
		# is executed only when the notification button is pressed. Previously the
		# direct call caused immediate scheduling of `_mark_handled`, auto-handling
		# the train.
		btn = Button("Mark handled", on_pressed=self._mark_handled)

		# Attempt to await send if it's a coroutine; otherwise fall back to sync call/create
		await self.notifier.send(title=f"Train #{train_index} arriving", sound=DEFAULT_SOUND,message=f"Global: {global_timer_display}",buttons=[btn])
			

	def _run_async_loop(self):
		asyncio.set_event_loop(self._async_loop)
		self._async_loop.run_forever()

	async def _create_notifier(self):
		return DesktopNotifier(app_name="AdCom Train Timer")

	def _inc_index(self):
		if self.current_train_index < MAX_TRAIN_INDEX:
			self.current_train_index += 1
			self.idx_var.set(str(self.current_train_index))
			self.time_until_next = self.train_intervals[self.current_train_index]
			self.next_time_var.set(format_seconds(self.time_until_next))

	def _dec_index(self):
		if self.current_train_index > 0:
			self.current_train_index -= 1
			self.idx_var.set(str(self.current_train_index))
			self.time_until_next = self.train_intervals[self.current_train_index]
			self.next_time_var.set(format_seconds(self.time_until_next))

	def _toggle_start(self):
		self.train_running = not self.train_running
		self.start_btn.config(text="Stop" if self.train_running else "Start")
		self.status_var.set("Running" if self.train_running else "Paused")

	def _mark_handled(self):
		# Called when user handles the train
		if not self.global_running:
			# starting global timer when first handled
			self.global_running = True
			self.global_timer = GLOBAL_TIMER
			self.status_var.set("Global timer started")

		# If global timer expired at handling, reset sequence
		if self.global_timer <= 0:
			self.current_train_index = 0
		else:
			# advance index but cap
			if self.current_train_index < MAX_TRAIN_INDEX:
				self.current_train_index += 1
		self.idx_var.set(str(self.current_train_index))
		self.time_until_next = self.train_intervals[self.current_train_index]
		self.next_time_var.set(format_seconds(self.time_until_next))
		self.arrived = False
		self.notified = False

	def _reset_global(self):
		self.global_running = False
		self.global_timer = GLOBAL_TIMER
		self.global_time_var.set(format_seconds(self.global_timer))
		self.status_var.set("Global reset")

	def _toggle_cal(self):
		self.cal_running = not self.cal_running
		if self.cal_running:
			self.cal_time = 0
			self.cal_start_btn.config(text="Stop Cal")
			self.status_var.set("Calibrating")
		else:
			self.cal_start_btn.config(text="Start Cal")
			self.status_var.set("Idle")

	def _mark_calibrated(self):
		# stop calibration and set index according to measured time
		if not self.cal_running and self.cal_time == 0:
			return
		self.cal_running = False
		self.cal_start_btn.config(text="Start Cal")
		measured = self.cal_time
		# find first interval strictly greater than measured, otherwise last
		chosen = MAX_TRAIN_INDEX
		for i, v in enumerate(self.train_intervals):
			if v > measured:
				chosen = i
				break
		self.current_train_index = chosen
		self.idx_var.set(str(self.current_train_index))
		self.time_until_next = self.train_intervals[self.current_train_index]
		self.next_time_var.set(format_seconds(self.time_until_next))
		# start timers immediately
		self.train_running = True
		self.start_btn.config(text="Stop")
		if not self.global_running:
			self.global_running = True
			self.global_timer = GLOBAL_TIMER
		self.status_var.set(f"Calibrated: {format_seconds(measured)} -> idx {chosen}")

	def _update_loop(self):
		# called every 1s via after
		if self.train_running:
			self.time_until_next -= 1
			if self.time_until_next < 0:
				self.time_until_next = 0
			self.next_time_var.set(format_seconds(self.time_until_next))
			# notify 15s before arrival
			if self.time_until_next <= 15 and not self.notified:
				self.notified = True
				asyncio.run_coroutine_threadsafe(self._desktop_notification(), self._async_loop)
			if not self.arrived and self.time_until_next == 0:
				self.arrived = True
				self.status_var.set("Train arrived")

		if self.global_running:
			self.global_timer -= 1
			if self.global_timer < 0:
				self.global_timer = 0
			self.global_time_var.set(format_seconds(self.global_timer))

		# calibration timer
		if self.cal_running:
			self.cal_time += 1
			self.cal_var.set(format_seconds(self.cal_time))

		# schedule next tick
		self.after(1000, self._update_loop)

	def run(self):
		self.mainloop()


if __name__ == "__main__":
	app = AdComTrainTimer()
	app.run()






