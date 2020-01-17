import aeconvert
controller.set("Keyframes", {
    "Speed": aeconvert.convert(controller.appctx.get_resource("scripts/keys2.txt")) * 0.5,
    "Displace": 0.2 + aeconvert.convert(controller.appctx.get_resource("scripts/keys2.txt")) * 0.2,
})
