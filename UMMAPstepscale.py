import streamlit as st
import pandas as pd
import datetime
import requests

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False
if 'prior_experience' not in st.session_state:
    st.session_state.prior_experience = None
if 'phone_number' not in st.session_state:
    st.session_state.phone_number = None
if 'earliest_date' not in st.session_state:
    st.session_state.earliest_date = None
if 'external_experience' not in st.session_state:
    st.session_state.external_experience = None
if 'IDrow' not in st.session_state:
    st.session_state.IDrow = None

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

# Load data
@st.cache_data
def load_data():
    Roster = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAProster.csv'
    STEP = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPpayscale.csv'
    TITLE = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPtitleScale.csv'
    
    roster = pd.read_csv(Roster)
    titles = pd.read_csv(TITLE)
    steps = pd.read_csv(STEP)
    return roster, titles, steps

roster, titles, steps = load_data()

# Main app logic with pages
if st.session_state.page == 1:
    st.header("Employee Information Verification")
    IDinput = st.number_input('Can I get your employee ID number?', min_value=0)
    
    if IDinput > 0:
        try:
            IDrow = roster[roster['EMPLID'] == IDinput]
            if not IDrow.empty:
                st.session_state.IDrow = IDrow  # Store in session state
                st.write(f"OK, great. The data we have from the University says that you are a {IDrow['JOBCODE_DESCR'].iloc[0]}, "
                        f"that you started work in that title on {IDrow['MIN_APPT_START_DATE'].iloc[0]} and your "
                        f"current full-time salary rate is ${IDrow['ANNUAL_FTR'].iloc[0]:,.2f}. Is all that correct?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes, that's correct"):
                        st.session_state.page = 2
                        st.rerun()
                with col2:
                    if st.button("No, that's not correct"):
                        st.session_state.page = 'error'
                        st.rerun()
            else:
                st.error("Employee ID not found in our records.")
        except Exception as e:
            st.error(f"Error processing employee data: {e}")

elif st.session_state.page == 'error':
    st.write("OK, that means there's an error somewhere and I'll need to get back to you.")
    phone_number = st.text_input("What's the best phone number for you?")
    if phone_number:
        if submit_to_google_form(phone_number):
            st.success("Thank you! We'll contact you soon.")
            st.session_state.phone_number = phone_number
            if st.button("Continue"):
                st.session_state.page = 'end'
                st.rerun()

elif st.session_state.page == 2:
    if st.session_state.IDrow is not None:
        start_date = st.session_state.IDrow['MIN_APPT_START_DATE'].iloc[0]
        st.write(f"Ok, so the next question is whether you have experience IN YOUR CURRENT JOB TITLE AT UM before {start_date}. "
                f"I.e. did you have a job in the same series, like Associate, Intermediate, Senior, Clinical Specialist, etc.?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes"):
                st.session_state.prior_experience = True
                st.session_state.page = 3
                st.rerun()
        with col2:
            if st.button("No"):
                st.session_state.prior_experience = False
                st.session_state.page = 4
                st.rerun()

elif st.session_state.page == 3:
    st.write("OK, what would be the earliest date you started working at UM including that experience?")
    earliest_date = st.date_input("Enter date", min_value=datetime.date(1950, 1, 1))
    if st.button("Continue"):
        st.session_state.earliest_date = earliest_date
        st.session_state.page = 4
        st.rerun()

elif st.session_state.page == 4:
    st.write("Ok, now I want to make sure that you understand I'm giving you our best calculation of where you'll end up. "
             "Since you've provided me with your own data, we have to think of this as a best estimate. OK?")
    if st.button("OK, I understand"):
        st.session_state.page = 5
        st.rerun()

elif st.session_state.page == 5:
    if st.session_state.IDrow is not None:
        # Calculate salary increase
        job_title = st.session_state.IDrow['JOBCODE_DESCR'].iloc[0]
        current_salary = st.session_state.IDrow['ANNUAL_FTR'].iloc[0]
        
        # Get scale from job title
        job_code_str = st.session_state.IDrow['JOBCODE_DESCR'].iloc[0]
        scale_row = titles[titles['Job Title'] == job_code_str]
        scale = scale_row['Scale'].iloc[0] if not scale_row.empty else "Unknown"
        
        # Calculate new salary (6% increase)
        new_salary = current_salary * 1.06
        increase_percent = 6

        st.write(f"Ok, great. What I'm seeing is that since you're a {job_title}, you're on scale {scale} "
                f"and that your salary will increase to ${new_salary:,.2f} in the first year. "
                f"That's retroactive to November 1 and it's an increase of {increase_percent}%.")
        
        st.write("Now for year two, do you have time in the same job NOT at UM--or do you have experience in a "
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
    st.write("OK, what's the experience?")
    experience = st.text_area("Please describe your experience:")
    if experience:
        st.session_state.external_experience = experience
        st.write("So what I can tell you is that that could make a difference in the second year, "
                "but it depends on our negotiations with management over what specific jobs come with what kind of credit. "
                "Does that make sense?")
        if st.button("Yes, makes sense"):
            st.session_state.page = 'end'
            st.rerun()

elif st.session_state.page == 7:
    if st.session_state.IDrow is not None:
        current_salary = st.session_state.IDrow['ANNUAL_FTR'].iloc[0]
        # Calculate future increases
        year2_increase = current_salary * (1.03 + 0.0125)
        year3_increase = year2_increase * (1.0225 + 0.0125)
        
        st.write("OK, that means you'll get the standard raise of 3% plus 1.25% in the second year "
                f"(approximately ${year2_increase:,.2f}) "
                "and 2.25% plus 1.25% in the third year "
                f"(approximately ${year3_increase:,.2f}).")
        if st.button("Continue"):
            st.session_state.page = 'end'
            st.rerun()

elif st.session_state.page == 'end':
    st.write("Great, nice to meet you!")
    if st.button("Start Over"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
