import streamlit as st
import pandas as pd

STEP = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPpayscale.csv'
TITLE = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPtitleScale.csv'
titles = pd.read_csv(TITLE)
steps = pd.read_csv(STEP)


# Assuming you have unique values you want to search through
search_options = titles['Job Title'].unique().tolist()

# This creates a searchable dropdown
selected_value = st.selectbox('Search', search_options)

# Filter based on exact match
filtered_title = titles[titles['Job Title'] == selected_value]

st.dataframe(filtered_title)

scale_letter = filtered_title.iloc[0]['Scale']

scale_input = st.text_input('Enter your Scale (capital letter):', f'We think it\'s {scale_letter} based on your Title of {selected_value} and Jobe Code {filtered_title.iloc[0]["Job Code"]}')

try:
   current_salary = float(st.text_input('Enter amount:', 'Enter a number without commas or $ sign'))
except ValueError:
   st.error('Please enter a valid number')
BaseMin_25 = current_salary * 1.06

guidelines = """
Add up total years in your current UM job title, including:
- All jobs in same series (Associate, Intermediate, Senior, Clinical Specialist)
- Non-Registered job experience when certified
- Grad Non-Cert experience for permanent title
- Mammography Tech → Mammography Dual Tech
- Orthotist/Prosthetist experience counts for either role
- All ultrasound/vascular/MSK/cardiac sonographer experience counts for each other
- Allied Health Tech Coordinator as Polysomnographic Tech counts for Polysomnographic experience
- Histology Tech experience counts for Medical Tech roles
"""

st.write(guidelines)

try:
   years = float(st.text_input('Enter total years in current job title:', 'Enter number of years'))
except ValueError:
   st.error('Please enter a valid number of years')


step_row = steps[steps['STEPS'] == years]

alt_base = step_row[scale_input].iloc[0]

salary_guess = max(alt_base, BaseMin_25)


# Find row with closest value
closest_row = steps.iloc[(steps[scale_input] - BaseMin_25).abs().argsort()[:1]]
BaseMinStep = closest_row['STEPS'].iloc[0]


st.write(f"We think your 2025 salary will be {salary_guess} based on a step of {max(years, BaseMinStep)}")
