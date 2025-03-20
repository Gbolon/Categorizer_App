# List of valid exercises and their categories
VALID_EXERCISES = {
    'Torso': [
        'Straight Arm Trunk Rotation (Dominant)',
        'Straight Arm Trunk Rotation (Non-Dominant)',
        'Shot Put (Countermovement) (Dominant only)'
    ],
    'Arms': [
        'PNF D2 Flexion (Dominant)',
        'PNF D2 Extension (Dominant)',
        'PNF D2 Flexion (Non-Dominant)',
        'PNF D2 Extension (Non-Dominant)',
        'Biceps Curl (One Hand) (Dominant)',
        'Triceps Extension (One Hand) (Dominant)',
        'Biceps Curl (One Hand) (Non-Dominant)',
        'Triceps Extension (One Hand) (Non-Dominant)'
    ],
    'Press/Pull': [
        'Horizontal Row (One Hand) (Dominant)',
        'Horizontal Row (One Hand) (Non-Dominant)',
        'Chest Press (One Hand) (Dominant)',
        'Chest Press (One Hand) (Non-Dominant)'
    ],
    'Legs': [
        'Lateral Bound (Dominant)',
        'Lateral Bound (Non-Dominant)',
        'Vertical Jump (Countermovement)'
    ]
}

# Flatten exercise list for validation
ALL_EXERCISES = [exercise for category in VALID_EXERCISES.values() for exercise in category]
