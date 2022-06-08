"""
Copyright (c) 2022, Miles Frantz
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""

import os, sys, json

class wrapper():
	def __init__(self, latestStep: str, localDataFile:str=None, load: bool = False):
		self.setlatestStep = latestStep
		self.call_path = []
		self.local = localDataFile or "writing_temp_output.csv"
		self.current_results = None

	def __getitem__(self, key):
		if not isinstance(key, str) or key not in self.current_results.keys():
			return None
		return self.current_results[key]

	def __setitem__(self, key, value):
		if not isinstance(key, str):
			return None
		self.current_results[key] = value

	def __enter__(self):
		print(f"Starting at step {self.setlatestStep}")
		if os.path.exists(self.local):
			with open(self.local, "rb") as reader:
				self.current_results = json.load(reader)
			os.remove(self.local)
		else:
			self.current_results = {
				'CallChain':[]
			}

		self['LatestStep'] = self.setlatestStep
		self['CallChain'] += [self.setlatestStep]
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			os.remove(self.local)
		except:
			pass

		def json_cap(obj):
			if isinstance(obj,set):
				return list(obj)
			return TypeError

		with open(self.local, "w+") as writer:
			json.dump(self.current_results, writer, default=json_cap)

		print(f"Exiting at step {self.setlatestStep}")
		return self

	@property
	def clean(self):
		for ext in [".xlsx", ".csv", ".png", ".jpg", ".json", ".puml", ".svg"]:
			try:
				os.system(f"yes|rm -r *{ext}")
			except:
				pass
		return

	def keys(self):
		return self.current_results.keys()

	def values(self):
		return self.current_results.values()

	def items(self):
		return self.current_results.items()

	def msg(self, string: str = ""):
		string = string or ""
		print(string)

	def get_last_working_step(self, get_last: int = 2):
		synthed, ktr = dc(self['CallChain']), 0
		synthed.reverse()
		for step in synthed:
			ktr += 1
			if ktr == get_last:
				return step
		return None
