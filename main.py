import ugfx, pyb, buttons, dialogs, wifi
from mqtt import MQTTClient

TICK_EVERY_MS = 100

# Graphics setup
ugfx.init()
ugfx.clear()
buttons.init()
sty = ugfx.Style(dialogs.default_style_badge)
sty.set_enabled([ugfx.WHITE, ugfx.html_color(0xA66FB0), ugfx.html_color(0x5e5e5e), ugfx.RED])
sty.set_background(ugfx.html_color(0xA66FB0))
ugfx.set_default_style(sty)
ugfx.area(0,0,320,240,sty.background())
ugfx.set_default_font(ugfx.FONT_MEDIUM)
ugfx.backlight(30)
LINE_HEIGHT = 20

current_line = 0
def write_line(text):
    global current_line
    ugfx.text(5, 5 + (current_line * LINE_HEIGHT), text, ugfx.WHITE)
    print(text)
    current_line += 1

# This will immediately return if we're already connected, otherwise
# it'll attempt to connect or prompt for a new network. Proceeding
# without an active network connection will cause the getaddrinfo to
# fail.
wifi.connect(
    wait=True,
    show_wait_message=False,
    prompt_on_fail=True,
    dialog_title='TiLDA Wifi'
)

# mqtt setup
def sub_cb(topic, msg):
    write_line(topic + " - " + msg)

channel = b"channel"
session_id = "emfbadge_" + str(pyb.rng())
mqtt = MQTTClient(session_id, "sandbox-mqtt.ably.io", user="mz3G9w.G3yQww", password="Rjo9T6rLAKaK64wu", keepalive=60)
mqtt.set_callback(sub_cb)
write_line("connecting to server...")
res = mqtt.connect()
write_line("connect result: " + str(res))

def on_tick(now):
    global last_ping
    # Non-blocking wait for message
    mqtt.check_msg()
    if now - last_ping >= 5*1000: ## TODO change back to 60
        # mqtt.ping()
        print(".")
        mqtt.publish(channel, b"hello world")
        last_ping = now

next_tick = 0
if res == 0:
    last_ping = pyb.millis()
    mqtt.subscribe(channel)
    mqtt.publish(channel, b"hello world")
    mqtt.publish(channel, b"hello world")
    mqtt.publish(channel, b"hello world")
    while True:
        pyb.wfi() # Wait For Input -- only waits 1ms
        ugfx.poll()

        now = pyb.millis()
        if (next_tick <= now):
            next_tick = now + TICK_EVERY_MS
            on_tick(now)


# mqtt.disconnect()

# while True:
    # pyb.wfi()
    # if buttons.is_triggered("BTN_MENU") or buttons.is_triggered("BTN_A") or buttons.is_triggered("BTN_B") or buttons.is_triggered("JOY_CENTER"):
        # break;

# ugfx.clear()
