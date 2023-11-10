TRAINING_COLUMNS = [
    "Make",
    "Price",
    "Year",
    "Kilometer",
    "Fuel Type",
    "Transmission",
    "Color",
    "Engine",
    "Drivetrain",
    "Length",
    "Width",
    "Height",
    "Seating Capacity",
    "Fuel Tank Capacity",
    "Max Power",
    "Max Torque",
]
SPLIT_COLUMNS = ["Max Power", "Max Torque"]
SPLIT_PATTERNS = {
    "Engine": "cc",
    "Max Power_left": "bhp",
    "Max Power_right": "rpm",
    "Max Torque_left": "nm",
    "Max Torque_right": "rpm",
}
ID_COLUMN = "item_id"
