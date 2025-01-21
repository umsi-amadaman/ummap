
import streamlit as st
import pandas as pd
import datetime as datetime

# Initialize session state
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False
   
def submit_to_google_form(phone_number):
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdgcNhzJYb91AjLijmKbrkeDQE7szinOh0F5jZfJcc_cwd-CA/formResponse"
    form_data = {
        'entry.526853801': phone_number
    }
    
    try:
        response = requests.post(FORM_URL, data=form_data)
        return response.ok
    except:
        return False



Roster = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAProster.csv'

roster = pd.read_csv(Roster)



IDinput = st.number_input(f'Please enter your Employee ID number')

IDrow = roster[roster['EMPLID'] == IDinput]


st.write(f'OK, great. The data we have from the University says that you are a
{IDrow['JOBCODE_DESCR'].iloc[0]}, that you started work in that title on {IDrow['MIN_APPT_START_DATE'].iloc[0]} and your
current full-time salary rate is ${IDrow[ANNUAL_FTR].iloc[0]}. Is all that correct?')

if st.button("Confirm"):
    st.session_state.confirmed = True
    st.write("Thank you for confirming!")

# In your Streamlit app
if not st.session_state.confirmed:
    phone_number = st.text_input("What's the best phone number for you?")
    if phone_number:
        if submit_to_google_form(phone_number):
            st.success("Thank you! We'll contact you soon.")


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

scale_input = st.text_input(f'Enter your Scale (a capital letter), we think it\'s {scale_letter} based on your Title of {selected_value} and Jobe Code {filtered_title.iloc[0]["Job Code"]}', scale_letter)

current_salary = 0.0
try:
   current_salary = float(st.number_input('Enter your current salary as a number without commas or $ sign'))
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

years = 0
try:
   years = float(st.number_input('Enter total years in current job title:', 1))
except ValueError:
   st.error('Please enter a valid number of years')


step_row = steps[steps['STEPS'] == years]

alt_base = step_row[scale_input].iloc[0]

salary_guess = max(alt_base, BaseMin_25)


# Find row with closest value
closest_row = steps.iloc[(steps[scale_input] - BaseMin_25).abs().argsort()[:1]]
BaseMinStep = closest_row['STEPS'].iloc[0]


st.write(f"We think your 2025 salary will be {salary_guess} based on a step of {max(years, BaseMinStep)}")
