import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    # Create base date
    base_date = datetime(2025, 1, 1)
    
    # Sample data for User 1
    user1_data = [
        # Chest Press (One Hand) - Shows time constraint effects
        {
            'user name': 'User1',
            'exercise name': 'Chest Press (One Hand)',
            'dominance': 'Dominant',
            'exercise createdAt': base_date,
            'power - high': 150,
            'acceleration - high': 200,
            'sex': 'male'
        },
        {
            'user name': 'User1',
            'exercise name': 'Chest Press (One Hand)',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=15),  # Too soon after first (15 days)
            'power - high': 155,
            'acceleration - high': 205,
            'sex': 'male'
        },
        {
            'user name': 'User1',
            'exercise name': 'Chest Press (One Hand)',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=60),  # Valid second test (60 days)
            'power - high': 160,
            'acceleration - high': 210,
            'sex': 'male'
        },
        {
            'user name': 'User1',
            'exercise name': 'Chest Press (One Hand)',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=200),  # Too long after previous (140 days)
            'power - high': 165,
            'acceleration - high': 215,
            'sex': 'male'
        },
        
        # Biceps Curl - Different exercise on consecutive days (should be fine)
        {
            'user name': 'User1',
            'exercise name': 'Biceps Curl (One Hand)',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=1),  # Day after Chest Press
            'power - high': 100,
            'acceleration - high': 150,
            'sex': 'male'
        },
        {
            'user name': 'User1',
            'exercise name': 'Biceps Curl (One Hand)',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=61),  # Valid second test
            'power - high': 110,
            'acceleration - high': 160,
            'sex': 'male'
        }
    ]
    
    # Sample data for User 2
    user2_data = [
        # PNF D2 Flexion - Perfect timing
        {
            'user name': 'User2',
            'exercise name': 'PNF D2 Flexion',
            'dominance': 'Dominant',
            'exercise createdAt': base_date,
            'power - high': 180,
            'acceleration - high': 220,
            'sex': 'female'
        },
        {
            'user name': 'User2',
            'exercise name': 'PNF D2 Flexion',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=70),  # Valid second test
            'power - high': 185,
            'acceleration - high': 225,
            'sex': 'female'
        },
        {
            'user name': 'User2',
            'exercise name': 'PNF D2 Flexion',
            'dominance': 'Dominant',
            'exercise createdAt': base_date + timedelta(days=140),  # Valid third test
            'power - high': 190,
            'acceleration - high': 230,
            'sex': 'female'
        }
    ]
    
    # Combine all data
    all_data = pd.DataFrame(user1_data + user2_data)
    
    # Save to CSV
    all_data.to_csv('sample_exercise_data.csv', index=False)
    return 'sample_exercise_data.csv'

if __name__ == "__main__":
    generate_sample_data()
