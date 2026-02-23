import json
import random

sequence = [[random.random() for _ in range(99)] for _ in range(30)]

payload = {
    "athlete_id": 1,
    "sequence": sequence,
    "heart_rate": 80,
    "body_temperature": 37,
    "hydration_level": 0.8,
    "sleep_quality": 7,
    "recovery_score": 6,
    "stress_level": 4,
    "muscle_activity": 0.6,
    "joint_angles": 45,
    "gait_speed": 5,
    "cadence": 170,
    "step_count": 5000,
    "jump_height": 0.4,
    "ground_reaction_force": 1200,
    "range_of_motion": 60,
    "ambient_temperature": 30,
    "humidity": 50,
    "altitude": 200,
    "training_intensity": 0.7,
    "training_duration": 60,
    "training_load": 300,
    "fatigue_index": 0.5
}

print(json.dumps(payload))