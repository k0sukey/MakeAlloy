MakeAlloy is Sublime Text 2 plugin. cmd + b = build alloy!

## How to install and usage

1. Make dir ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MakeAlloy
2. Copy MakeAlloy.* to ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MakeAlloy
3. Edit the ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/MakeAlloy/MakeAlloy.sublime-settings file to the correct path for the Alloy
4. Restart Sublime Text 2
5. Go to menu Tools > Build System > select MakeAlloy
6. cmd + b > select platform

## iOS device build setting
1. Prefereces > Package Settings > MakeAlloy > Settings - User
2. Your provisioning profile uuid and iOS Developer user name

```
{
	"provisioning": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
	"developer": "Kosuke Isobe"
}
```

## iOS device transfer setting
1. Required [ideviceinstaller](http://cgit.sukimashita.com/ideviceinstaller.git/) ```$ brew install ideviceinstaller```
2. Prefereces > Package Settings > MakeAlloy > Settings - User
3. Your device uuid

```
{
	"device": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

### iOS device transfer usage
1. cmd + b
2. build iphone(or ipad) device
3. transfer iphone(or ipad) device

## ChangeLog
* Added iOS device build
* Dealing with Alloy 1.0.0 (Build for Titanium CLI command)
* MakeAlloy.sublime-settings

## Inspierd

[MakeTi](https://github.com/appersonlabs/MakeTi).
