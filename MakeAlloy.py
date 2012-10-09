import sublime, sublime_plugin, subprocess

class MakeAlloyCommand(sublime_plugin.WindowCommand):
	s = sublime.load_settings("MakeAlloy.sublime-settings")
	proc = subprocess.Popen("ls -1 " + s.get("titaniumsdk"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = proc.communicate()
	sdk = out.splitlines()

	def run(self, *args, **kwargs):
		print args, kwargs
		self.window.show_quick_panel(self.sdk, self._quick_panel_callback)

	def _quick_panel_callback(self, index):
		root = self.window.folders()[0]
		self.window.run_command("exec", {"cmd": ["alloy", "-t", self.sdk[index], "run", root]})
