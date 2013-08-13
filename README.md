arDMX
=====

A DMX lighting controller. This project includes both a hardware element powered by an Arduino which drives a RS485 adaptor chip which is then used to drive the DMX lighting circuit; and also simple control software. The control software is based around a simple web interface which is driven from a python webapp.

Todo
----
* Server actually connects to arduino and sets values
* Support for select box light values as opposed to sliders
* Server stores current light values which are restored by the page at load time
* Implement fading over a period of time with client side updating values using timers

License
-------
MIT [http://witchard.mit-license.org](http://witchard.mit-license.org)

