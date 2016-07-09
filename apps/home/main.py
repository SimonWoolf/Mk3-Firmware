import ugfx
import pyb

def display_name():
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0xFFFF)
	ugfx.set_default_font("D*")
	ugfx.text(40,90,"My name is...",ugfx.BLUE)
	ugfx.text(40,120,"MATT",ugfx.BLUE)
	ugfx.circle(140,200,40,ugfx.GREEN)
	ugfx.circle(160,200,40,ugfx.GREEN)
	ugfx.circle(180,200,40,ugfx.GREEN)

def button_press():
	import apps.home.quick_launch
	apps.home.quick_launch.main()


	display_name()
	pyb.delay(1500)

def main():
	display_name()

	tgl_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
	tgl_menu.init(pyb.Pin.IN, pyb.Pin.PULL_UP)

	while True:
		pyb.wfi()
		if tgl_menu.value() == 0:
			button_press()

ugfx.init()
main()
