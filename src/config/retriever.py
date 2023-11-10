NUMERIC_IMPUTER_STRATEGY = "median"
CATEGORICAL_IMPUTER_STRATEGY = "most_frequent"
N_CANDIDATES = 30
DISTANCE_METRIC = "cosine"

# split features into groups can be done programmatically but I like to have control
NUMERIC_FEATURES = [
    "Price",
    "Year",
    "Kilometer",
    "Engine",
    "Length",
    "Width",
    "Height",
    "Seating Capacity",
    "Fuel Tank Capacity",
    "Max Power_left",
    "Max Power_right",
    "Max Torque_left",
    "Max Torque_right",
]
CATEGORICAL_FEATURES = ["Make", "Fuel Type", "Transmission", "Color", "Drivetrain"]
