import streamlit as st

# Title of the application
st.title("Dynamic Form Example")

# Sidebar for dynamic form selection
st.sidebar.title("Job Titles")
form_type = st.sidebar.selectbox("Choose job title", ["Anasthesia Technician", "Athletic Trainer", "Art Therapist", "Audiologist"])

# Function to create a job form
def create_Anasthesia_Technician():
    JobTitle = "Anasthesia Technician"
    st.header("Contact Info")
    name = st.text_input("Name")
    email = st.text_input("Email")
    EmpID = st.text_input("Employee ID")

    st.header("Direct Experience: Enter number of years")
    DirectExp = st.number_input("Anesthesiology Tech", min_value=0, max_value=40, step=1)

    st.header("Highly Related Experience: Enter number of years.")
    MedicalAssistant = st.number_input("Medical Assistant", min_value=0, max_value =40, step=1)
    PatientCareTechnician = st.number_input("Patient Care Technician", min_value=0, max_value =40, step=1)
    SurgicalTechnologist = st.number_input("Surgical Technologist", min_value=0, max_value =40, step=1)
    NurseAssistant = st.number_input("Nurse Assistant", min_value=0, max_value =40, step=1)
    Phlebotomist = st.number_input("Phlebotomist", min_value=0, max_value =40, step=1)
    PharmacyTechnician = st.number_input("Pharmacy Technician", min_value=0, max_value =40, step=1)

    st.header("Related Experience: Enter number of years")
    MedicalRecordsTechnician = st.number_input("Medical Records Technician", min_value=0, max_value =40, step=1)
    CallCenterRepresentative = st.number_input("Call Center Representative", min_value=0, max_value =40, step=1)
    PatientServicesAssistant = st.number_input("Patient Services Assistantn", min_value=0, max_value =40, step=1)
		

    if st.button("Submit"):
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Employee ID: {EmpID}")
        st.write(f"Job Title: {JobTitle}")
        st.write(f"Direct Experience: {DirectExp}")

        HRExpCalc = (MedicalAssistant + PatientCareTechnician + SurgicalTechnologist + Phlebotomist + PharmacyTechnician) #*.75
        #HRExp = min(HRExpCalc, 5)
        st.write(f"Highly Related Experience: {HRExpCalc}")

        RExpCalc = (MedicalRecordsTechnician + CallCenterRepresentative + PatientServicesAssistant) #*.25
        #RExp = min(RExpCalc, 2)
        st.write(f"Related Experience: {RExpCalc}")


def create_Athletic_Trainer():
    JobTitle = "Athletic Trainer"
    st.header("Contact Info")
    name = st.text_input("Name")
    email = st.text_input("Email")
    EmpID = st.text_input("Employee ID")

    st.header("Direct Experience: Enter number of years")
    DirectExp = st.number_input("Athletic Trainer", min_value=0, max_value=40, step=1)

    st.header("Additional Experience")
    SpecialtyExperienceCertification = st.number_input("Specialty Experience/Certification", min_value=0, max_value =2, step=1)
    AdditionalHRE = st.number_input("Additional Higher or Related Experience", min_value=0, max_value =2, step=1)
		
    if st.button("Submit"):
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Employee ID: {EmpID}")
        st.write(f"Job Title: {JobTitle}")
        st.write(f"Direct Experience: {DirectExp}")

        HRExpCalc = SpecialtyExperienceCertification + AdditionalHRE 
        #HRExp = min(HRExpCalc, 2)
        st.write(f"Highly Related Experience: {HRExpCalc}")


def create_Art_Therapist():
    JobTitle = "Art Therapist"
    st.header("Contact Info")
    name = st.text_input("Name")
    email = st.text_input("Email")
    EmpID = st.text_input("Employee ID")

    st.header("Direct Experience: Enter number of years")
    ArtTherapist = st.number_input("Art Therapist", min_value=0, max_value=40, step=1)
    ATFellowship = st.number_input("AT Fellowship", min_value=0, max_value=40, step=1)


    st.header("Highly Related Experience: Enter number of years") #. 75% credit up to 5.25 points.")
    ActivityRecreationTherapy = st.number_input("Acivity/Recreation Therapy", min_value=0, max_value =40, step=1)
    ArtTeacher = st.number_input("Art Teacher", min_value=0, max_value =40, step=1)
    Counselor = st.number_input("Child Life/Mental Health Support/Counselor", min_value=0, max_value =40, step=1)
    AdjunctProfessor = st.number_input("AdjunctProfessor", min_value=0, max_value =40, step=1)


    st.header("Related Experience: Enter number of years") #. 50% credit up to 2.5 points.")
    NonArtFormalTeaching = st.number_input("Non-Art Formal Teaching (schools/child development centers)", min_value=0, max_value =40, step=1)
    ProgramExperience = st.number_input("Program Experience (Paid Position)", min_value=0, max_value =40, step=1)
    DirectPatientCare = st.number_input("Other Healthcare experience (direct patient care)", min_value=0, max_value =40, step=1)
    VisualArtsMultimedia = st.number_input("Visual Arts/Multimedia", min_value=0, max_value =40, step=1)
    ResearchPosition = st.number_input("Research Position", min_value=0, max_value =40, step=1)

    st.header("Education Credit (Max $2000)")
    options = ["Ph.D. ($2000)", "Additional Masters beyond Required ($1500)"]
    # Dictionary to store the binary states
    binary_states = {}
    EdCredit = 0

    # Display checkboxes and set binary states
    st.subheader("Select Options:")
    is_1checked = st.checkbox(options[0])
    is_2checked = st.checkbox(options[1])
    if is_1checked:
        EdCredit = 2000
    elif is_2checked:
        EdCredit = 1500

    st.header("Certification Credit, enter 1 for each ceritification, max 1 point")
    ATRBS = st.number_input("ATR-BS", min_value=0, max_value =1, step=1)
    CTRS = st.number_input("CTRS", min_value=0, max_value =1, step=1)
    MTBC = st.number_input("MT-BC", min_value=0, max_value =1, step=1)
    LLPC = st.number_input("LLPC", min_value=0, max_value =1, step=1)
    LLP = st.number_input("LLP", min_value=0, max_value =1, step=1)
    LMSW = st.number_input("LMSW", min_value=0, max_value =1, step=1)
    InfantMassage = st.number_input("Infant Massage (0.5 points)", min_value=0, max_value =1, step=1)
    FLE = st.number_input("Family Life Educator (0.5 points)", min_value=0, max_value =1, step=1)
    CPXP = st.number_input("CPXP (0.5 points)", min_value=0, max_value =1, step=1)

    if st.button("Submit"):
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Employee ID: {EmpID}")
        st.write(f"Job Title: {JobTitle}")


        DirectExp = ArtTherapist + ATFellowship
        st.write(f"Direct Experience: {DirectExp}")

        HRExpCalc = (ActivityRecreationTherapy + ArtTeacher + Counselor + AdjunctProfessor) # * .75
        #HRExp = min(HRExpCalc, 5.25)
        st.write(f"Highly Related Experience: {HRExpCalc}")

        RExpCalc = (NonArtFormalTeaching + ProgramExperience + DirectPatientCare + VisualArtsMultimedia + ResearchPosition) # *.5
        #RExp = min(RExpCalc, 2.5)
        st.write(f"Related Experience: {RExpCalc}")

        st.write(f"Ed Credit: {EdCredit}")
        CCcalc = (ATRBS + MTBC + CTRS + LLP + LLPC + LMSW) + 0.5*(InfantMassage + FLE + CPXP)
        #CertCredit = min(CCcalc, 1)
        st.write(f"Certification Credit: {CCcalc}")

def create_Audiologist():
    JobTitle = "Audiologist"
    st.header("Contact Info")
    name = st.text_input("Name")
    email = st.text_input("Email")
    EmpID = st.text_input("Employee ID")

    st.header("Direct Experience: Enter number of years")
    DirectExp = st.number_input("Audiologist", min_value=0, max_value=40, step=1)

    st.header("Highly Related Experience: Enter number of years. 75% credit up to 5 points.")
    HRExpCalc = st.number_input("Audiologist in alternate setting (Pediatrics for Adult etc)", min_value=0, max_value =40, step=1)

    st.header("Certification Credit, enter 1 for each ceritification, max 1 point")
    AmericanSign = st.number_input("American Sign Language Certification (0.5 points)", min_value=0, max_value =1, step=1)
    Deaf = st.number_input("Deaf/Hard of hearing Teaching Certificaiton (0.5 points)", min_value=0, max_value =1, step=1)
    
    if st.button("Submit"):
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Employee ID: {EmpID}")
        st.write(f"Job Title: {JobTitle}")

        st.write(f"Direct Experience: {DirectExp}")

        #HRExp = min(0.75*HRExpCalc, 5)
        st.write(f"Highly Related Experience: {HRExpCalc}")


        st.write(f"Ed Credit: {EdCredit}")
        #CCcalc = 0.5*(AmericanSign + Deaf)
        #CertCredit = min(CCcalc, 1)
        st.write(f"Certification Credit: {EdCredit}")


# Display the selected form
if form_type == "Anasthesia Technician":
    create_Anasthesia_Technician()
elif form_type == "Athletic Trainer":
    create_Athletic_Trainer()
elif form_type == "Art Therapist":
    create_Art_Therapist()
elif form_type == "Audiologist":
    create_Audiologist()
