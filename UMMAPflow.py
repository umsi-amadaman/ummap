import streamlit as st
import pandas as pd
import datetime
import requests
from datetime import datetime

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.update({
        'page': 1,
        'IDrow': None,
        'prior_experience': None,
        'earliest_date': None,
        'external_experience': None,
        'phone_number': None
    })

def submit_to_google_form(phone_number):
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdgcNhzJYb91AjLijmKbrkeDQE7szinOh0F5jZfJcc_cwd-CA/formResponse"
    try:
        response = requests.post(FORM_URL, data={'entry.526853801': phone_number})
        return response.ok
    except:
        return False

@st.cache_data
def load_data():
    base_url = "https://github.com/umsi-amadaman/UMMAP/raw/main/"
    files = {
        'roster': 'UMMAProster.csv',
        'titles': 'UMMAPtitleScale.csv',
        'steps': 'UMMAPpayscale.csv',
        'full': 'ummapfull.csv'
    }
    return {k: pd.read_csv(f"{base_url}{v}") for k, v in files.items()}

def calculate_salary_increase(row, titles, steps):
    job_title = row['JOBCODE_DESCR'].iloc[0]
    current_salary = row['ANNUAL_FTR'].iloc[0]
    
    # Get scale from job title
    scale_row = titles[titles['Job Title'] == job_title]
    if scale_row.empty:
        return None, None, None
        
    scale = scale_row['Scale'].iloc[0]
    
    # Calculate years on job
    job_entry_date = pd.to_datetime(row['JOB_ENTRY_DT'].iloc[0])
    years_on_job = (datetime(2025, 2, 15) - job_entry_date).days / 365.25
    
    # Calculate 6% increase
    min_increase = current_salary * 1.06
    
    # Get step based on years
    step_salary = steps[steps['Scale'] == scale].iloc[int(years_on_job)]['Salary']
    
    # Use higher of the two
    new_salary = max(min_increase, step_salary)
    increase_percent = ((new_salary - current_salary) / current_salary) * 100
    
    return scale, new_salary, increase_percent

data = load_data()

# Main app logic
if st.session_state.page == 1:
    st.header("Employee Information Verification")
    IDinput = st.number_input('Can I get your employee ID number?', min_value=0)
    
    if IDinput > 0:
        IDrow = data['full'][data['full']['Emplid'] == IDinput]
        if not IDrow.empty:
            st.session_state.IDrow = IDrow
            st.write(f"OK, great. The data we have from the University says that your name is {IDrow['First Name'].iloc[0]} {IDrow['Last Name'].iloc[0]}, "
                    f"are a {IDrow['JOBCODE_DESCR'].iloc[0]}, that you started work on {IDrow['JOB_ENTRY_DT'].iloc[0]}, "
                    f"and that your current full-time salary rate is ${IDrow['ANNUAL_FTR'].iloc[0]:,.2f}. Is all that correct?")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Yes"):
                    st.session_state.page = 2
                    st.rerun()
            with col2:
                if st.button("Only Job Entry Date Wrong"):
                    st.session_state.page = 'date_correction'
                    st.rerun()
            with col3:
                if st.button("Other Information Wrong"):
                    st.session_state.page = 'error'
                    st.rerun()
        else:
            st.error("ID number not found. I'll have someone get back to you.")
            phone_number = st.text_input("What's a good phone number?")
            if phone_number and submit_to_google_form(phone_number):
                st.session_state.phone_number = phone_number
                st.success("Thank you! We'll contact you soon.")

elif st.session_state.page == 'date_correction':
    st.write("OK, what should the correct date be?")
    corrected_date = st.date_input("Enter correct date", min_value=datetime.date(1950, 1, 1))
    if st.button("Continue"):
        st.session_state.IDrow['JOB_ENTRY_DT'] = corrected_date
        st.session_state.page = 2
        st.rerun()

elif st.session_state.page == 'error':
    st.write("That means there's an error in the data we got from management.")
    phone_number = st.text_input("What's a good phone number?")
    if phone_number and submit_to_google_form(phone_number):
        st.session_state.phone_number = phone_number
        st.success("Thank you! We'll contact you soon.")
        if st.button("Start Over"):
            st.session_state.clear()
            st.rerun()

elif st.session_state.page == 2:
    if 'JOBCODE_DESCR' in st.session_state.IDrow.columns and 'Social Worker' in st.session_state.IDrow['JOBCODE_DESCR'].iloc[0]:
        st.write("I see you're a social worker. Are you on the clinical ladder at all?")
        if st.button("Yes"):
            st.session_state.page = 'error'
            st.rerun()
        elif st.button("No"):
            st.session_state.page = 3
            st.rerun()
    else:
        st.write(f"Do you have experience IN YOUR CURRENT JOB TITLE AT UM before {st.session_state.IDrow['JOB_ENTRY_DT'].iloc[0]}?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes"):
                st.session_state.page = 3
                st.rerun()
        with col2:
            if st.button("No"):
                st.session_state.page = 4
                st.rerun()

elif st.session_state.page == 3:
    st.write("What would be the earliest date you started working at UM including that experience?")
    earliest_date = st.date_input("Enter date", min_value=datetime.date(1950, 1, 1))
    if st.button("Continue"):
        st.session_state.earliest_date = earliest_date
        st.session_state.page = 4
        st.rerun()

elif st.session_state.page == 4:
    st.write("I want to make sure you understand I'm giving you our best calculation of where you'll end up. "
             "Since you've provided me with your own data, we have to think of this as a best estimate. OK?")
    if st.button("I understand"):
        st.session_state.page = 5
        st.rerun()

elif st.session_state.page == 5:
    if st.session_state.IDrow is not None:
        scale, new_salary, increase_percent = calculate_salary_increase(
            st.session_state.IDrow, data['titles'], data['steps']
        )
        
        if None not in (scale, new_salary, increase_percent):
            st.write(f"Since you're a {st.session_state.IDrow['JOBCODE_DESCR'].iloc[0]}, "
                    f"you're on scale {scale}. Your salary will increase to ${new_salary:,.2f} "
                    f"in the first year. That's retroactive to November 1 and it's an increase of {increase_percent:.1f}%.")
            
            st.write("For year two, do you have time in the same job NOT at UM--or experience in a "
                    "related job that we didn't count, either at UM or not at UM?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes"):
                    st.session_state.page = 6
                    st.rerun()
            with col2:
                if st.button("No"):
                    st.session_state.page = 7
                    st.rerun()

elif st.session_state.page == 6:
    st.write("What's the experience?")
    experience = st.text_area("Please describe:")
    if experience:
        st.session_state.external_experience = experience
        st.write("That could make a difference in the second year, "
                "but it depends on our negotiations with management over what specific jobs come with what kind of credit.")
        if st.button("I understand"):
            st.session_state.page = 'end'
            st.rerun()

elif st.session_state.page == 7:
    current_salary = st.session_state.IDrow['ANNUAL_FTR'].iloc[0]
    year2_increase = current_salary * 1.0425  # 3% + 1.25%
    year3_increase = year2_increase * 1.035   # 2.25% + 1.25%
    
    st.write("You'll get these standard raises:")
    st.write(f"• Year 2: 3% plus 1.25% (approximately ${year2_increase:,.2f})")
    st.write(f"• Year 3: 2.25% plus 1.25% (approximately ${year3_increase:,.2f})")
    
    if st.button("Continue"):
        st.session_state.page = 'end'
        st.rerun()

elif st.session_state.page == 'end':
    st.write("Great, nice to meet you!")
    if st.button("Start Over"):
        st.session_state.clear()
        st.rerun()
