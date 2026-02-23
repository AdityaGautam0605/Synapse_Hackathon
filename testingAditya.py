# import json
# import random

# sequence = [[random.random() for _ in range(99)] for _ in range(30)]

# payload = {
#     "athlete_id": 1,
#     "sequence": sequence,
#     "heart_rate": 80,
#     "body_temperature": 37,
#     "hydration_level": 0.8,
#     "sleep_quality": 7,
#     "recovery_score": 6,
#     "stress_level": 4,
#     "muscle_activity": 0.6,
#     "joint_angles": 45,
#     "gait_speed": 5,
#     "cadence": 170,
#     "step_count": 5000,
#     "jump_height": 0.4,
#     "ground_reaction_force": 1200,
#     "range_of_motion": 60,
#     "ambient_temperature": 30,
#     "humidity": 50,
#     "altitude": 200,
#     "training_intensity": 0.7,
#     "training_duration": 60,
#     "training_load": 300,
#     "fatigue_index": 0.5
# }

# with open("test_payload.json", "w") as f:
#     json.dump(payload, f)

import json
import numpy as np
import random

# Generate valid LSTM sequence (30 x 99)
sequence = np.random.rand(30, 99).tolist()

payload = {
    "athlete_id": 1,

    # LSTM sequence
    "sequence": sequence,

    # Biometric
    "heart_rate": random.uniform(60, 180),
    "body_temperature": random.uniform(36.0, 39.0),
    "hydration_level": random.uniform(0.3, 1.0),
    "sleep_quality": random.uniform(0.0, 1.0),
    "recovery_score": random.uniform(0.0, 1.0),
    "stress_level": random.uniform(0.0, 1.0),
    "muscle_activity": random.uniform(0.0, 1.0),
    "joint_angles": random.uniform(0.0, 180.0),
    "gait_speed": random.uniform(0.5, 5.0),
    "cadence": random.uniform(60, 200),
    "step_count": random.uniform(1000, 20000),
    "jump_height": random.uniform(0.1, 1.5),
    "ground_reaction_force": random.uniform(100, 2000),
    "range_of_motion": random.uniform(0.0, 180.0),

    # Environment
    "ambient_temperature": random.uniform(10, 40),
    "humidity": random.uniform(20, 90),
    "altitude": random.uniform(0, 3000),

    # Training
    "training_intensity": random.uniform(0.0, 1.0),
    "training_duration": random.uniform(10, 180),
    "training_load": random.uniform(100, 1000),
    "fatigue_index": random.uniform(0.0, 1.0),

    # Optional label
    "injury_occurred": 0
}

with open("test_payload.json", "w") as f:
    json.dump(payload, f, indent=4)

print("test_payload.json created successfully.")