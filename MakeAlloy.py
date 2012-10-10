import sublime, sublime_plugin, subprocess

class MakeAlloyCommand(sublime_plugin.WindowCommand):
	instance_list = ["iphone", "android", "mobileweb", "clean", "generate view", "generate controller", "generate widget", "generate jmk", "generate migration", "generate model"]

	def run(self, *args, **kwargs):
		print args, kwargs
		self.window.show_quick_panel(self.instance_list, self._quick_panel_callback)

	def _quick_panel_callback(self, index):
		if (index > -1):
			root = self.window.folders()[0]

			if (self.instance_list[index] == "clean"):
				subprocess.call("rm -rf " + root + "/build/iphone/; mkdir -p " + root + "/build/iphone",
					shell=True)
				subprocess.call("rm -rf " + root + "/build/android/; mkdir -p " + root + "/build/android",
					shell=True)
				sublime.status_message("Deleted build/iphone/*, build/android/*")
			elif (self.instance_list[index] == "generate view"
				or self.instance_list[index] == "generate controller"
				or self.instance_list[index] == "generate widget"
				or self.instance_list[index] == "generate jmk"
				or self.instance_list[index] == "generate migration"
				or self.instance_list[index] == "generate model"):
				self.alloy = "alloy " + self.instance_list[index]
				self.window.show_input_panel(self.alloy, '', self._input_panel_callback, None, None)
			else:
				cat = subprocess.Popen("cat " + root + "/tiapp.xml",
					stdout=subprocess.PIPE,
					shell=True)

				grep = subprocess.Popen("grep '<sdk-version>'",
					stdin=cat.stdout,
					stdout=subprocess.PIPE,
					shell=True)

				sed = subprocess.Popen("sed -e 's/<\/*sdk-version>//g'",
					stdin=grep.stdout,
					stdout=subprocess.PIPE,
					shell=True)
				sdk, err = sed.communicate()

				self.window.run_command("exec", {"cmd": ["alloy", "-t", sdk.strip(), "run", root, self.instance_list[index]]})

	def _input_panel_callback(self, text):
		root = self.window.folders()[0]
		cmd = self.alloy.split(' ')
		self.window.run_command("exec", {"cmd": ["alloy", "-o", root + "/app", "generate", cmd[2], text]})
