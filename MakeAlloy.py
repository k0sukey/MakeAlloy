import os
import sublime
import sublime_plugin
import subprocess


class MakeAlloyCommand(sublime_plugin.WindowCommand):
    settings = sublime.load_settings("MakeAlloy.sublime-settings")
    os.environ["PATH"] = str(settings.get('path'))
    panel = ["run iphone simulator", "run ipad simulator", "run android emulator", "transfer android device", "compile", "clean", "generate view", "generate controller", "generate widget", "generate jmk", "generate migration", "generate model"]

    def run(self, *args, **kwargs):
        # print args, kwargs
        self.root = self.window.folders()[0]
        self.window.show_quick_panel(self.panel, self._quick_panel_callback)

    def _quick_panel_callback(self, index):
        if (index > -1):
            if (self.panel[index] == "clean"):
                self.window.run_command("exec", {"cmd": ["titanium", "clean", "--no-colors", "-d", self.root]})
            elif (self.panel[index] == "generate jmk"):
                self.window.run_command("exec", {"cmd": ["alloy", "-n", "-o", self.root + "/app", "generate", "jmk"]})
            elif (self.panel[index] == "generate view"
                    or self.panel[index] == "generate controller"
                    or self.panel[index] == "generate widget"
                    or self.panel[index] == "generate migration"
                    or self.panel[index] == "generate model"):
                self.generate = "alloy " + self.panel[index]
                self.window.show_input_panel("alloy", '', self._input_panel_callback, None, None)
            else:
                cat = subprocess.Popen("cat '" + self.root + "/tiapp.xml'",
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

                self.window.run_command("exec", {"cmd": ["alloy", "-n", "-t", sdk.strip(), "compile", self.root]})

                if (self.panel[index] != "compile"):
                    options = self.panel[index].split(' ')
                    if (options[1] == "iphone" or options[1] == "ipad"):
                        self.window.run_command("exec", {"cmd": ["titanium", "build", "--no-colors", "-s", sdk.strip(), "-p", "ios", "-T", options[2], "-F", options[1], "-d", self.root, "--log-level", str(self.settings.get('loglevel'))]})
                    else:
                        self.window.run_command("exec", {"cmd": ["titanium", "build", "--no-colors", "-s", sdk.strip(), "-p", "android", "-T", options[2], "-A", str(self.settings.get('androidsdk')), "-d", self.root, "--log-level", str(self.settings.get('loglevel'))]})

    def _input_panel_callback(self, text):
        cmd = self.generate.split(' ')
        self.window.run_command("exec", {"cmd": ["alloy", "-n", "-o", self.root + "/app", "generate", cmd[2], text]})
