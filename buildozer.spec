[app]

title = VERDIN
package.name = verdin
package.domain = org.verdin
source.dir = .
source.include_exts = py,kv,png,jpg,atlas
version = 1.0.0

requirements = python3,kivy,requests,pyjnius

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.permissions = INTERNET, RECORD_AUDIO

[buildozer]

log_level = 2
warn_on_root = 1
