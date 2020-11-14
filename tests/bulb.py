from yeelight import Bulb

bulb = Bulb("192.168.1.72",effect="smooth")

bulb.start_music(2000)
bulb.set_rgb(255, 0, 0)
