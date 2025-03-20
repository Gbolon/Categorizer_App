# List of valid exercises and their categories
VALID_EXERCISES = {
    'Torso': [
        'Straight Arm Trunk Rotation',
        'Straight Arm Trunk Rotation (Plyo)',
        'Shot Put (Countermovement)'
    ],
    'Arms': [
        'PNF D2 Flexion',
        'PNF D2 Extension',
        'Biceps Curl (One Hand)',
        'Biceps Curl (Two Hand)',
        'Triceps Extension (One Hand)',
        'Triceps Extension (Two Hand)'
    ],
    'Press/Pull': [
        'Horizontal Row (One Hand)',
        'Horizontal Row (Two Hand)',
        'Chest Press (One Hand)',
        'Chest Press (Two Hand)'
    ],
    'Legs': [
        'Lateral Bound',
        'Vertical Jump (Countermovement)'
    ]
}

# Define which exercises require dominance and valid dominance values
EXERCISE_DOMINANCE = {
    'Straight Arm Trunk Rotation': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Straight Arm Trunk Rotation (Plyo)': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Shot Put (Countermovement)': {'required': False, 'values': []},
    'PNF D2 Flexion': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'PNF D2 Extension': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Biceps Curl (One Hand)': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Biceps Curl (Two Hand)': {'required': False, 'values': []},
    'Triceps Extension (One Hand)': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Triceps Extension (Two Hand)': {'required': False, 'values': []},
    'Horizontal Row (One Hand)': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Horizontal Row (Two Hand)': {'required': False, 'values': []},
    'Chest Press (One Hand)': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Chest Press (Two Hand)': {'required': False, 'values': []},
    'Lateral Bound': {'required': True, 'values': ['Dominant', 'Non-Dominant']},
    'Vertical Jump (Countermovement)': {'required': False, 'values': []}
}

def standardize_dominance(dominance):
    """Convert dominance string to standard format."""
    if not dominance:
        return None

    dominance = str(dominance).strip().lower()
    if dominance == 'dominant':
        return 'Dominant'
    elif dominance == 'non-dominant':
        return 'Non-Dominant'
    return dominance

def is_valid_exercise_dominance(exercise_name, dominance):
    """Validate if exercise name and dominance combination is valid."""
    if exercise_name not in EXERCISE_DOMINANCE:
        return False

    exercise_config = EXERCISE_DOMINANCE[exercise_name]
    if not exercise_config['required']:
        return True

    standardized_dominance = standardize_dominance(dominance)
    return standardized_dominance in exercise_config['values']

def get_full_exercise_name(exercise_name, dominance=None):
    """Generate full exercise name with dominance if required."""
    if not exercise_name in EXERCISE_DOMINANCE:
        return None

    if EXERCISE_DOMINANCE[exercise_name]['required']:
        standardized_dominance = standardize_dominance(dominance)
        if standardized_dominance:
            return f"{exercise_name} ({standardized_dominance})"
    return exercise_name

# Generate list of all possible exercise variations
ALL_EXERCISES = []
for exercises in VALID_EXERCISES.values():
    for exercise in exercises:
        if EXERCISE_DOMINANCE[exercise]['required']:
            ALL_EXERCISES.extend([
                get_full_exercise_name(exercise, "Dominant"),
                get_full_exercise_name(exercise, "Non-Dominant")
            ])
        else:
            ALL_EXERCISES.append(exercise)