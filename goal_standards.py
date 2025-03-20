"""Goal standards for exercise movements based on sex."""

POWER_STANDARDS = {
    'male': {
        'Straight Arm Trunk Rotation': 250,
        'Shot Put (Countermovement)': 300,
        'PNF D2 Flexion': 180,
        'PNF D2 Extension': 180,
        'Biceps Curl (One Hand)': 150,
        'Triceps Extension (One Hand)': 150,
        'Horizontal Row (One Hand)': 200,
        'Chest Press (One Hand)': 200,
        'Lateral Bound': 400,
        'Vertical Jump (Countermovement)': 450
    },
    'female': {
        'Straight Arm Trunk Rotation': 200,
        'Shot Put (Countermovement)': 250,
        'PNF D2 Flexion': 150,
        'PNF D2 Extension': 150,
        'Biceps Curl (One Hand)': 120,
        'Triceps Extension (One Hand)': 120,
        'Horizontal Row (One Hand)': 160,
        'Chest Press (One Hand)': 160,
        'Lateral Bound': 350,
        'Vertical Jump (Countermovement)': 400
    }
}

ACCELERATION_STANDARDS = {
    'male': {
        'Straight Arm Trunk Rotation': 25,
        'Shot Put (Countermovement)': 30,
        'PNF D2 Flexion': 20,
        'PNF D2 Extension': 20,
        'Biceps Curl (One Hand)': 15,
        'Triceps Extension (One Hand)': 15,
        'Horizontal Row (One Hand)': 20,
        'Chest Press (One Hand)': 20,
        'Lateral Bound': 35,
        'Vertical Jump (Countermovement)': 40
    },
    'female': {
        'Straight Arm Trunk Rotation': 20,
        'Shot Put (Countermovement)': 25,
        'PNF D2 Flexion': 18,
        'PNF D2 Extension': 18,
        'Biceps Curl (One Hand)': 12,
        'Triceps Extension (One Hand)': 12,
        'Horizontal Row (One Hand)': 18,
        'Chest Press (One Hand)': 18,
        'Lateral Bound': 30,
        'Vertical Jump (Countermovement)': 35
    }
}

def get_base_exercise_name(full_exercise_name):
    """Extract base exercise name from full name including dominance."""
    if '(' in full_exercise_name:
        return full_exercise_name.split('(')[0].strip()
    return full_exercise_name

def calculate_development_score(value, exercise_name, sex, metric_type='power'):
    """Calculate development score as percentage of goal standard."""
    if not value or pd.isna(value):
        return None
        
    base_exercise = get_base_exercise_name(exercise_name)
    standards = POWER_STANDARDS if metric_type == 'power' else ACCELERATION_STANDARDS
    
    if sex not in standards or base_exercise not in standards[sex]:
        return None
        
    goal_standard = standards[sex][base_exercise]
    return (value / goal_standard) * 100 if goal_standard else None
