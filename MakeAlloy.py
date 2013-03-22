# coding: utf-8

import os
import sublime
import sublime_plugin
import subprocess

settings = {}


# Load Settings
def load_settings():
    global settings
    settings = sublime.load_settings("MakeAlloy.sublime-settings")
    # PATH normalization
    os_path = os.environ["PATH"].split(":")
    settings_path = settings.get("path").split(":")
    path = os_path + settings_path
    path = sorted(set(path), key=path.index)
    os.environ["PATH"] = ":".join(path)

# Lazy load
sublime.set_timeout(load_settings, 1500)


class MakeAlloyCommand(sublime_plugin.WindowCommand):
    global settings
    panel = [
        "run iphone simulator", "build iphone device", "run ipad simulator", "build ipad device",
        "run android emulator", "transfer android device",
        "compile", "clean", "generate view", "generate controller", "generate widget",
        "generate jmk", "generate migration", "generate model"
    ]

    def run(self, *args, **kwargs):
        self.root = self.window.folders()[0]
        self.window.show_quick_panel(self.panel, self.quick_panel_callback)
        return True

    def execmd(self, cmd_arr):
        self.window.run_command("exec", {
            "cmd": cmd_arr
        })

    def quick_panel_callback(self, index):
        if index > -1:
            # Clean
            if self.panel[index] == "clean":
                self.execmd(["titanium", "--no-colors", "clean", "-d", self.root])
            # Generate jmk
            elif self.panel[index] == "generate jmk":
                self.execmd(["alloy", "-n", "-o", self.root + "/app", "generate", "jmk"])
            # Generate View, Controller, Widget, Migration, Model
            elif self.panel[index] == "generate view" or\
                self.panel[index] == "generate controller" or\
                self.panel[index] == "generate widget" or\
                self.panel[index] == "generate migration" or\
                    self.panel[index] == "generate model":
                self.generate = "alloy " + self.panel[index]
                self.window.show_input_panel(self.generate, "", self.input_panel_callback, None, None)
            # Running, Compile
            else:
                # Prepare
                cat = subprocess.Popen("cat '" + self.root + "/tiapp.xml'", stdout=subprocess.PIPE, shell=True)
                grep = subprocess.Popen("grep '<sdk-version>'", stdin=cat.stdout, stdout=subprocess.PIPE, shell=True)
                sed = subprocess.Popen("sed -e 's/<\/*sdk-version>//g'", stdin=grep.stdout, stdout=subprocess.PIPE, shell=True)
                sdk, err = sed.communicate()
                sdk = sdk.decode("utf-8").strip()

                # Pre compile
                self.execmd(["alloy", "-n", "-t", sdk, "compile", self.root])

                # Running
                if not self.panel[index] == "compile":
                    options = (self.panel[index].split(" "))[1:3]
                    platform = options[0]
                    target = options[1]
                    # iOS
                    if platform == "iphone" or platform == "ipad":
                        # Slimulator
                        if target == "simulator":
                            self.execmd(["titanium", "--no-colors", "build", "-s", sdk, "-p", "ios",
                                        "-T", target, "-d", self.root, "--log-level", self.settings.get("loglevel")])
                        # Device
                        else:
                            self.execmd(["titanium", "--no-colors", "build", "-s", sdk, "-p", "ios",
                                        "-V", self.settings.get("developer"),
                                        "-P", self.settings.get("provisioning"),
                                        "-T", target, "-d", self.root, "--log-level", self.settings.get("loglevel")])
                    # Android
                    else:
                        self.execmd(["titanium", "build", "--no-colors", "-s", sdk, "-p", "android",
                                    "-T", target, "-A", self.settings.get("androidsdk"),
                                    "-d", self.root, "--log-level", self.settings.get("loglevel")])
        else:
            return True

    def input_panel_callback(self, text):
        cmd = self.generate.split(" ")
        self.execmd(["alloy", "-n", "-o", self.root + "/app", "generate", cmd[2], text])
