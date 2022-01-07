from src.classes.hardware import Hardware


def water_plant(seconds: int) -> None:
    print(f"-> Watering Plant For {str(seconds)} Seconds")
    plant = Hardware(26)
    plant.water_cycle(seconds)
    plant.cleanup()
    print("-> Done.")
