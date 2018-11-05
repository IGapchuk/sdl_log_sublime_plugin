# sdl_sublime_log_plugin
Sublime Text plugin  for handy work with SDL logs.

##Requirements
This plugin requires at least Sublime Text 3 v.3176 or higher for best perfomance and correct syntax

## Installing
- Move directory "SDL Logs" to Sublime Packages folder.
(Generally at /home/*USER*/.config/sublime-text-3/Packages)
(Creating folder for plugin in Pacckages is good practise, you can choose any name for it)
- Necessary open "preferences->Package->Settings->SDL Logs->Setting" and change attribute "source_path" on own path to source sdl_core.
- Change syntax in Sublime to SDL Logs.
(View -> Syntax ->SDL Logs)

## Functionality
This plugin implements color scheme and simple commands to work with SDL logs
- Indicates methods and make them clickable (Opens file containing that method and highlight him)
- Search for common syntax patterns and highlight them (color scheme)
- Implements commands for filtering columns&strings, finding not closed functions

## Configuration
Open Sublime in top panel choose preferences->Packege->Settings->SDL Logs:
- Item "Color Scheme" contain configuration for text color.
- Item "Setting" contain all path to configurate files and path to your sources.
- Item "Key Bindings" contain all keybings configuration.
