import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.update({
        'page': 1,
        'IDrow': None,
        'prior_experience': None,
        'earliest_date': None,
        'corrected_date': None,
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


roster = pd.read_csv('https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAProster.csv')
titles = pd.read_csv('https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPtitleScale.csv')
steps = pd.read_csv('https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPpayscale.csv')
full = pd.read_csv('https://github.com/umsi-amadaman/UMMAP/raw/main/ummapfull.csv', dtype={'EmplID': str})


def calculate_salary_increase():
   jobcode = str(st.session_state.IDrow['Jobcode'].iloc[0])
   #st.write(jobcode, type(jobcode))
   currentsalary = st.session_state.IDrow['Comp Annual Rt'].iloc[0]
   if st.session_state.corrected_date:
       job_entry = pd.to_datetime(st.session_state.corrected_date)
   elif st.session_state.earliest_date:
       job_entry = pd.to_datetime(st.session_state.earliest_date)
   else:
       job_entry = pd.to_datetime(st.session_state.IDrow['Job Entry Dt'].iloc[0])
   
   scale = titles.loc[titles['Job Code'] == jobcode, 'Scale'].iloc[0]
   
   years = (datetime.now() - job_entry).days / 365.25
   step_salary = steps[scale].iloc[int(years)]
   min_salary = currentsalary * 1.06
   
   new_salary = max(step_salary, min_salary)
   increase = ((new_salary - currentsalary) / currentsalary) * 100
   
   return scale, new_salary, increase

# Main app logic
if st.session_state.page == 1:
    st.header("Employee Information Verification")
    IDinput = st.text_input('Can I get your employee ID number?')
    
    if IDinput:
        IDrow = full[full['EmplID'].astype(str) == IDinput]
        if not IDrow.empty:
            st.session_state.IDrow = IDrow
            st.write(f"OK, great. The data we have from the University says that your name is {IDrow['First Name'].iloc[0]} {IDrow['Last Name'].iloc[0]}, "
                    f"are a {IDrow['Jobcode Descr'].iloc[0]}, that you started work on {IDrow['Job Entry Dt'].iloc[0]}, "
                    f"and that your current full-time salary rate is ${IDrow['Comp Annual Rt'].iloc[0]:,.2f}. Is all that correct?")
            
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
                if st.button("Name, Job Title or Salary is wrong"):
                    st.session_state.page = 'error'
                    st.rerun()
        else:
            st.error("OK, for some reason that ID number isn’t showing up. I’ll have someone get back to you.")
            phone_number = st.text_input("What's a good phone number?")
            if phone_number and submit_to_google_form(phone_number):
                st.session_state.phone_number = phone_number
                st.success("Thank you! We'll contact you soon.")

elif st.session_state.page == 'date_correction':
    st.write("OK, what should the correct date be?")
    corrected_date = st.date_input("Enter correct date", min_value=date(1950, 1, 1))
    if st.button("Continue"):
        st.session_state.corrected_date = corrected_date
        st.session_state.page = 2
        st.rerun()

elif st.session_state.page == 'error':
    st.write("Ok, that means there's an error in the data we got from management. I'll have someone get back to you.")
    phone_number = st.text_input("What's a good phone number?")
    if phone_number and submit_to_google_form(phone_number):
        st.session_state.phone_number = phone_number
        st.success("Thank you! We'll contact you soon.")
        if st.button("Start Over"):
            st.session_state.clear()
            st.rerun()

elif st.session_state.page == 2:
   if 'Jobcode Descr' in st.session_state.IDrow.columns and 'Social Worker' in st.session_state.IDrow['Jobcode Descr'].iloc[0]:
       st.write("I see you're a social worker. Are you on the clinical ladder at all?")
       if st.button("Yes"):
           st.write("Ok, that makes things a little tricky. I'll have someone get back to you.")
           phone_number = st.text_input("What's a good phone number?")
           if phone_number and submit_to_google_form(phone_number):
               st.success("Thank you! We'll contact you soon.")
               st.session_state.clear()
               st.rerun()
       elif st.button("No"):
           st.session_state.page = 3 
           st.rerun()
   else:
        st.write(
    f"""
Ok, so the next question is whether you have experience before {st.session_state.IDrow['Job Entry Dt'].iloc[0]} in your current job SERIES AT UM 
, like Associate, Intermediate, Senior, Clinical Specialist, etc.?

Or do any of the following apply?

- Any Non-Registered job experience will count for the relevant job title when certified.
- Mammography Technologist experience will count for Mammography Dual Technologist.
- Orthotist, Prosthetist, and Orthotist and Prosthetist experience will all count for each other.
- All ultrasound technologist, vascular ultrasound technologist, msk technologist, and cardiac 
  sonographer non-invasive technologist experience will count for each other.
- Allied Health Technical Coordinator experience while performing as Polysomnographic 
  Technician (or lead) will count towards Polysomnographic experience.
- Histology Technician experience will count for Medical Technologists or Medical 
  Technologist Specialist.
"""
)

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
    earliest_date = st.date_input("Enter date", min_value=date(1950, 1, 1))
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
        scale, new_salary, increase_percent = calculate_salary_increase()
        st.session_state.new_salary = new_salary
        
        if None not in (scale, new_salary, increase_percent):
            st.write(f"Since you're a {st.session_state.IDrow['Jobcode Descr'].iloc[0]}, "
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
    current_salary = st.session_state.IDrow['Comp Annual Rt'].iloc[0]
    year2_increase = st.session_state.new_salary * 1.0425  # 3% + 1.25%
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
