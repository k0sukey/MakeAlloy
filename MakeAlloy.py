import sublime, sublime_plugin, subprocess

class MakeAlloyCommand(sublime_plugin.WindowCommand):
	instance_list = ["iphone", "android", "mobileweb", "clean"]

	def run(self, *args, **kwargs):
		print args, kwargs
		self.window.show_quick_panel(self.instance_list, self._quick_panel_callback)

	def _quick_panel_callback(self, index):
		if (index > -1):
			root = self.window.folders()[0]

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

			if (self.instance_list[index] == "clean"):
				subprocess.call("rm -rf " + root + "/build/iphone/; mkdir -p " + root + "/build/iphone",
					shell=True)
				subprocess.call("rm -rf " + root + "/build/android/; mkdir -p " + root + "/build/android",
					shell=True)
				sublime.status_message("Deleted build/iphone/*, build/android/*")
			else:
				self.window.run_command("exec", {"cmd": ["alloy", "-t", sdk.strip(), "run", root, self.instance_list[index]]})
