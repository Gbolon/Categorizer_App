# List of valid exercises and their categories
VALID_EXERCISES = {
    'Torso': [
        'Straight Arm Trunk Rotation',
        'Shot Put (Countermovement)'
    ],
    'Arms': [
        'PNF D2 Flexion',
        'PNF D2 Extension',
        'Biceps Curl (One Hand)',
        'Triceps Extension (One Hand)'
    ],
    'Press/Pull': [
        'Horizontal Row (One Hand)',
        'Chest Press (One Hand)'
    ],
    'Legs': [
        'Lateral Bound',
        'Vertical Jump (Countermovement)'
    ]
}

# Define which exercises require dominance
REQUIRES_DOMINANCE = {
    'Straight Arm Trunk Rotation': True,
    'Shot Put (Countermovement)': False,
    'PNF D2 Flexion': True,
    'PNF D2 Extension': True,
    'Biceps Curl (One Hand)': True,
    'Triceps Extension (One Hand)': True,
    'Horizontal Row (One Hand)': True,
    'Chest Press (One Hand)': True,
    'Lateral Bound': True,
    'Vertical Jump (Countermovement)': False
}

def get_full_exercise_name(exercise_name, dominance=None):
    """Generate full exercise name with dominance if required."""
    if REQUIRES_DOMINANCE[exercise_name] and dominance:
        return f"{exercise_name} ({dominance})"
    return exercise_name

# Generate list of all possible exercise variations
ALL_EXERCISES = []
for exercises in VALID_EXERCISES.values():
    for exercise in exercises:
        if REQUIRES_DOMINANCE[exercise]:
            ALL_EXERCISES.extend([
                get_full_exercise_name(exercise, "Dominant"),
                get_full_exercise_name(exercise, "Non-Dominant")
            ])
        else:
            ALL_EXERCISES.append(exercise)