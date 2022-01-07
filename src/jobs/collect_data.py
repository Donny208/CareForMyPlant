# Libraries
import os
from datetime import datetime
from dotenv import load_dotenv
from src.database.schema import Data

# Classes
from src.classes.miflora import MiFlora

# Pre-Setup
load_dotenv()
miflora = MiFlora(os.getenv("MIFLORA_MAC"))

# Main
plant_data = miflora.get_data()

db_data = Data()
db_data.timestamp = datetime.now().strftime("%Y/%m/%d %H:%M")
db_data.temperature = plant_data['temp']
db_data.moisture = plant_data['moist']
db_data.light = plant_data['light']
db_data.conductivity = plant_data['conduct']
db_data.battery = plant_data['battery']
db_data.save()
