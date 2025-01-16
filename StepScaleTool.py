import streamlit as st
import pandas as pd

# Set Streamlit page configuration (optional)
st.set_page_config(page_title="UMMAP Salary Predictor", layout="wide")

# URLs for data
STEP_URL = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPpayscale.csv'
TITLE_URL = 'https://github.com/umsi-amadaman/UMMAP/raw/main/UMMAPtitleScale.csv'

@st.cache_data
def load_data():
    """
    Load titles and steps data from CSV URLs.
    Caches the data to prevent reloading on every interaction.
    """
    try:
        titles_df = pd.read_csv(TITLE_URL)
        steps_df = pd.read_csv(STEP_URL)
        return titles_df, steps_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

titles, steps = load_data()

# Check if data loaded successfully
if titles.empty or steps.empty:
    st.stop()

# Sidebar (Optional for better UI)
st.sidebar.header("UMMAP Salary Predictor")

# Main Header
st.header("UMMAP Salary Predictor")

# Job Title Selection
search_options = titles['Job Title'].unique().tolist()
selected_value = st.selectbox('Select Your Job Title', search_options)

# Filter titles based on selection
filtered_title = titles[titles['Job Title'] == selected_value]

if not filtered_title.empty:
    st.subheader("Job Details")
    st.dataframe(filtered_title)
    
    # Extract scale and job code
    scale_letter = filtered_title.iloc[0].get('Scale', None)
    job_code = filtered_title.iloc[0].get('Job Code', 'N/A')  # Ensure correct column name
    
    if pd.isna(scale_letter):
        st.error("Scale information is missing for the selected job title.")
        st.stop()
    
    # Informative Message
    st.info(
        f"We think it's **{scale_letter}** based on your Title of **{selected_value}** and Job Code **{job_code}**."
    )
    
    # Scale Selection using selectbox to ensure valid input
    scale_options = sorted(titles['Scale'].dropna().unique().tolist())
    default_scale_index = scale_options.index(scale_letter) if scale_letter in scale_options else 0
    scale_input = st.selectbox(
        'Select Your Scale (Capital Letter)',
        options=scale_options,
        index=default_scale_index,
        help="Select the scale corresponding to your position."
    )
    
    # Current Salary Input using number_input for validation
    current_salary = st.number_input(
        'Enter Your Current Salary',
        min_value=0.0,
        step=1000.0,
        format="%.2f",
        help='Enter a number without commas or $ sign'
    )
    
    BaseMin_25 = current_salary * 1.06
    
    # Guidelines Section
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
    
    # Total Years Input using number_input for validation
    years = st.number_input(
        'Enter Total Years in Current Job Title',
        min_value=0.0,
        step=0.1,
        format="%.1f",
        help='Enter number of years'
    )
    
    # Debugging: Display steps DataFrame columns and selected scale
    st.write("**Steps DataFrame Columns:**", steps.columns.tolist())
    st.write("**Selected Scale Input:**", scale_input)
    st.write("**Entered Years:**", years)
    
    # Validate 'years' against STEPS
    if 'STEPS' not in steps.columns:
        st.error("The 'STEPS' column is missing from the steps data.")
        st.stop()
    
    # Ensure 'STEPS' is integer if appropriate
    if not pd.api.types.is_integer_dtype(steps['STEPS']):
        try:
            steps['STEPS'] = steps['STEPS'].astype(int)
        except ValueError:
            st.error("The 'STEPS' column contains non-integer values.")
            st.stop()
    
    # Convert years to integer for exact match
    step_years = int(years)
    step_row = steps[steps['STEPS'] == step_years]
    
    if not step_row.empty:
        if scale_input in step_row.columns:
            alt_base = step_row.iloc[0][scale_input]
            try:
                alt_base = float(alt_base)
            except (ValueError, TypeError):
                st.error(f"The value for scale '{scale_input}' is invalid in the steps data.")
                st.stop()
            salary_guess = max(alt_base, BaseMin_25)
        else:
            st.error(f"Scale '{scale_input}' not found in the steps data.")
            st.stop()
    else:
        st.error(f"No step data found for {step_years} years. Please enter a valid number of years.")
        st.stop()
    
    # Find the closest step if exact step not found
    if step_row.empty:
        closest_step_index = (steps['STEPS'] - step_years).abs().argsort()[:1]
        closest_row = steps.iloc[closest_step_index]
        BaseMinStep = closest_row['STEPS'].iloc[0]
    else:
        BaseMinStep = step_years
    
    # Display the estimated salary
    st.success(
        f"We estimate your 2025 salary to be **${salary_guess:,.2f}** based on a step of **{BaseMinStep}**."
    )
else:
    st.error("Selected job title does not have corresponding details.")
