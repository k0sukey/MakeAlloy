import os
import sublime
import sublime_plugin
import subprocess


class MakeAlloyCommand(sublime_plugin.WindowCommand):
    settings = sublime.load_settings("MakeAlloy.sublime-settings")
    alloy = os.environ["ALLOY_PATH"] = str(settings.get('alloy'))
    os.environ["ALLOY_NODE_PATH"] = str(settings.get('node'))
    os.environ["PATH"] = os.environ["PATH"] + ":/usr/local/bin"
    panel = ["run iphone", "run android", "run mobileweb", "compile", "clean", "generate view", "generate controller", "generate widget", "generate jmk", "generate migration", "generate model"]

    def run(self, *args, **kwargs):
        # print args, kwargs
        self.root = self.window.folders()[0]
        self.window.show_quick_panel(self.panel, self._quick_panel_callback)

    def _quick_panel_callback(self, index):
        if (index > -1):
            if (self.panel[index] == "clean"):
                subprocess.call("rm -rf '" + self.root + "/build/iphone/'; mkdir -p '" + self.root + "/build/iphone'",
                                shell=True)
                subprocess.call("rm -rf '" + self.root + "/build/android/'; mkdir -p '" + self.root + "/build/android'",
                                shell=True)
                sublime.status_message("Deleted build/iphone/*, build/android/*")
            elif (self.panel[index] == "generate view"
                    or self.panel[index] == "generate controller"
                    or self.panel[index] == "generate widget"
                    or self.panel[index] == "generate jmk"
                    or self.panel[index] == "generate migration"
                    or self.panel[index] == "generate model"):
                self.generate = "alloy " + self.panel[index]
                self.window.show_input_panel(self.alloy, '', self._input_panel_callback, None, None)
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

                if (self.panel[index] == "compile"):
                    self.window.run_command("exec", {"cmd": [self.alloy, "-n", "-t", sdk.strip(), "compile", self.root]})
                else:
                    platform = self.panel[index].split(' ')
                    self.window.run_command("exec", {"cmd": [self.alloy, "-n", "-t", sdk.strip(), "run", self.root, platform[1]]})

    def _input_panel_callback(self, text):
        cmd = self.generate.split(' ')
        self.window.run_command("exec", {"cmd": [self.alloy, "-n -o", self.root + "/app", "generate", cmd[2], text]})
