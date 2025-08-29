import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime



# Function to extract make, model, and description from car title
def parse_car_title(title):
    # Common car makes for better parsing
    common_makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Audi', 
                   'Volkswagen', 'Nissan', 'Hyundai', 'Kia', 'Mazda', 'Mitsubishi', 
                   'Subaru', 'Lexus', 'Jeep', 'Volvo', 'Land Rover', 'Range Rover',
                   'Porsche', 'Fiat', 'Renault', 'Peugeot', 'Skoda', 'Seat', 'Opel',
                   'Cadillac', 'Infiniti', 'Acura', 'Chrysler', 'Dodge', 'Jaguar',
                   'Mini', 'Smart', 'Suzuki', 'Tesla', 'Buick', 'Lincoln', 'GMC']
    
    title = title.strip()
    make = "Unknown"
    model = "Unknown"
    description = title
    
    # Try to find a known make
    for known_make in common_makes:
        if title.startswith(known_make):
            make = known_make
            # The rest is model and description
            remaining = title[len(known_make):].strip()
            
            # Try to split model from description (model is usually first few words)
            parts = remaining.split(',', 1)
            if len(parts) > 1:
                model = parts[0].strip()
                description = parts[1].strip()
            else:
                # If no comma, try to split by space
                words = remaining.split()
                if len(words) > 1:
                    model = words[0]
                    description = ' '.join(words[1:])
                else:
                    model = remaining
            break
    
    return make, model, description

# Function to convert price to USD
def convert_price(price_str):
    if not price_str or price_str == 'N/A':
        return None
    
    # Extract currency symbol and amount
    currency_symbol = price_str[0] if price_str[0] in ['$', '֏', '€', '£'] else None
    amount_str = price_str[1:] if currency_symbol else price_str
    
    # Clean the amount string
    amount_str = amount_str.replace(',', '').strip()
    
    try:
        amount = float(amount_str)
        
        # Convert to USD if needed
        if currency_symbol == '$':
            return amount
        elif currency_symbol and currency_symbol in EXCHANGE_RATES:
            return amount * EXCHANGE_RATES[currency_symbol]
        else:
            # Assume it's already in USD if no symbol
            return amount
    except:
        return None

# Function to convert mileage to kilometers
def convert_mileage(mileage_str):
    if not mileage_str or mileage_str == 'N/A':
        return None
    
    # Extract numeric value and unit
    numbers = re.findall(r'\d+', mileage_str)
    if not numbers:
        return None
    
    value = float(''.join(numbers))
    
    # Check if it's in miles (մղոն) or kilometers (կմ)
    if 'մղոն' in mileage_str or 'miles' in mileage_str.lower():
        # Convert miles to km (1 mile = 1.60934 km)
        return value * 1.60934
    else:
        # Assume it's already in km
        return value

# Function to extract date from Armenian date string
def parse_armenian_date(date_str):
    if not date_str or date_str == 'N/A':
        return None
    
    # Map Armenian month names to English
    armenian_months = {
        'Հունվար': 'January',
        'Փետրվար': 'February',
        'Մարտ': 'March',
        'Ապրիլ': 'April',
        'Մայիս': 'May',
        'Հունիս': 'June',
        'Հուլիս': 'July',
        'Օգոստոս': 'August',
        'Սեպտեմբեր': 'September',
        'Հոկտեմբեր': 'October',
        'Նոյեմբեր': 'November',
        'Դեկտեմբեր': 'December'
    }
    
    try:
        # Extract date parts
        parts = date_str.split(',')
        if len(parts) < 2:
            return None
            
        # Extract day, month, year, and time
        date_part = parts[1].strip()
        date_parts = date_part.split()
        
        if len(date_parts) < 3:
            return None
            
        month_arm = date_parts[0]
        day = date_parts[1].rstrip(',')
        year = date_parts[2]
        
        # Convert Armenian month to English
        month = armenian_months.get(month_arm, month_arm)
        
        # Create date string
        date_string = f"{day} {month} {year}"
        
        # Parse to datetime object
        return datetime.strptime(date_string, '%d %B %Y')
    except:
        return None

