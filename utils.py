import pandas as pd
import numpy as np
import re

def convert_distance(value):
    """
    Convert string value to numeric distance in kilometers
    - If contains 'կ' (km): extract integers
    - If contains 'մ' (miles): extract integers and multiply by 1.6
    """
    try:
        # Remove commas and extract numeric part
        numeric_str = ''.join(filter(str.isdigit, str(value)))
        numeric_value = float(numeric_str) if numeric_str else np.nan
        
        # Check for Armenian letters
        if 'կ' in str(value):  # kilometers
            return numeric_value
        elif 'մ' in str(value):  # miles to km conversion
            return numeric_value * 1.6
        else:
            return np.nan  # or handle other cases as needed
    except:
        return np.nan


def extract_price_robust(value):
    """
    More robust price extraction:
    - Extracts dollar amounts even if not at the beginning
    - Handles various formats
    - Returns NaN for complex text
    """
    if pd.isna(value):
        return np.nan
    
    value_str = str(value).strip()
    
    # Simple case: string starts with dollar sign and number
    if value_str.startswith('$'):
        # Extract the numeric part after dollar sign
        numeric_part = value_str[1:].replace(',', '').strip()
        if numeric_part.replace('.', '').isdigit():
            return float(numeric_part)
    
    # Check if it's a simple dollar amount pattern anywhere in string
    dollar_patterns = [
        r'\$\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?',  # $10,000 or $10,000.00
        r'\$\s*\d+',  # $10000
    ]
    
    for pattern in dollar_patterns:
        match = re.search(pattern, value_str)
        if match:
            numeric_value = match.group().replace('$', '').replace(',', '').strip()
            if numeric_value.replace('.', '').isdigit():
                return float(numeric_value)
    
    # If text contains other information (like the Armenian text example)
    return np.nan


