import streamlit as st
import pandas as pd

# Load data
STEP_URL = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPpayscale.csv'
TITLE_URL = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPtitleScale.csv'

@st.cache_data
def load_data():
    titles_df = pd.read_csv(TITLE_URL)
    steps_df = pd.read_csv(STEP_URL)
    return titles_df, steps_df

titles, steps = load_data()

# Sidebar for Navigation (Optional)
st.sidebar.header("UMMAP Salary Predictor")

# Job Title Selection
st.header("UMMAP Salary Predictor")

search_options = titles['Job Title'].unique().tolist()
selected_value = st.selectbox('Select Your Job Title', search_options)

# Filter titles based on selection
filtered_title = titles[titles['Job Title'] == selected_value]

if not filtered_title.empty:
    st.subheader("Job Details")
    st.dataframe(filtered_title)

    # Extract scale and job code
    scale_letter = filtered_title.iloc[0].get('Scale', '')
    job_code = filtered_title.iloc[0].get('Job Code', 'N/A')

    # Scale Selection (Restricting to valid options)
    scale_options = titles['Scale'].unique().tolist()
    default_scale = scale_letter if scale_letter in scale_options else scale_options[0]
    scale_input = st.selectbox(
        'Select Your Scale (Capital Letter)',
        scale_options,
        index=scale_options.index(default_scale) if default_scale in scale_options else 0,
        help=f"We think it's {scale_letter} based on your Title of {selected_value} and Job Code {job_code}"
    )

    # Current Salary Input
    current_salary = st.number_input(
        'Enter Your Current Salary',
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        help='Enter a number without commas or $ sign'
    )

    BaseMin_25 = current_salary * 1.06

    # Guidelines
    guidelines = """
    **Guidelines for Calculating Total Years in Current UM Job Title:**
    - Include all jobs in the same series (Associate, Intermediate, Senior, Clinical Specialist)
    - Include non-Registered job experience when certified
    - Include graduate non-Cert experience for permanent titles
    - Mammography Tech → Mammography Dual Tech
    - Orthotist/Prosthetist experience counts for either role
    - All ultrasound/vascular/MSK/cardiac sonographer experience counts for each other
    - Allied Health Tech Coordinator as Polysomnographic Tech counts for Polysomnographic experience
    - Histology Tech experience counts for Medical Tech roles
    """
    st.markdown(guidelines)

    # Total Years Input
    years = st.number_input(
        'Enter Total Years in Current Job Title',
        min_value=0.0,
        step=0.1,
        format="%.1f",
        help='Enter number of years'
    )

    # Validate 'years' against STEPS
    if 'STEPS' in steps.columns:
        # Assuming 'STEPS' column contains integer steps, we might need to round or floor the years
        # For exact match, ensure 'years' is an integer or handle appropriately
        step_row = steps[steps['STEPS'] == int(years)]

        if not step_row.empty:
            if scale_input in step_row.columns:
                alt_base = step_row.iloc[0][scale_input]
                salary_guess = max(alt_base, BaseMin_25)

                # Find the closest step if exact step not found
                closest_step_index = (steps['STEPS'] - years).abs().argsort()[:1]
                closest_row = steps.iloc[closest_step_index]
                BaseMinStep = closest_row['STEPS'].iloc[0]

                st.success(
                    f"We estimate your 2025 salary to be ${salary_guess:,.2f} based on a step of {max(years, BaseMinStep)}."
                )
            else:
                st.error(f"Scale '{scale_input}' not found in steps data.")
        else:
            st.error(f"No step data found for {years} years. Please enter a valid number of years.")
    else:
        st.error("The 'STEPS' column is missing from the steps data.")
else:
    st.error("Selected job title does not have corresponding details.")
