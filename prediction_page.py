import streamlit as st
from sklearn.preprocessing import OrdinalEncoder
import matplotlib.pyplot as plt
import pandas as pd
import string
import pickle

#############################################

original_df = pd.read_csv("bone-marrow.csv")

inputs = ["Recipientgender","Stemcellsource","Donorage","Gendermatch","RecipientRh","ABOmatch","CMVstatus","DonorCMV","RecipientCMV","Riskgroup","Diseasegroup","HLAmatch","HLAmismatch","Antigen","Alel","Recipientage","Rbodymass","Disease_ALL","Disease_AML","Disease_chronic","Disease_lymphoma","Disease_nonmalignant"]
input_df = pd.DataFrame(0, columns=inputs, index=[0])


#############################################

st.markdown("# Survivabiility of Pediatric Patients with Bone Marrow Transplants")

#############################################

st.sidebar.markdown("# Input Transplant Recipient Patient Data")

st.sidebar.subheader('Patient Gender')
r_gender = st.sidebar.radio(
    label = 'Transplant Recipient\'s Gender:',
    options = ['Male', 'Female']
)
if (r_gender=="Male"):
    input_df.loc[0]["Recipientgender"] = 1
else:
    input_df.loc[0]["Recipientgender"] = 0

st.sidebar.subheader('Recipient Age')
r_age = st.sidebar.number_input(
    label='Enter Recipient Age (yrs)', min_value=0.0, max_value=100.0, value=10.0, step=0.1)
r_age = float(r_age)
r_age2 =(r_age-9.845508982)/5.243799627
input_df.loc[0,"Recipientage"] = r_age2

st.sidebar.subheader('Recipient Body Mass')
r_mass = st.sidebar.number_input(
    label='Enter Recipient Weight (lbs)', min_value=0.0, max_value=200.0, value=40.0, step=1.0)
r_mass = float(r_mass)
r_mass2 =(r_mass-35.6005988)/19.2463758
input_df.loc[0, "Rbodymass"] = r_mass2

st.sidebar.subheader('Recipient Rh')
rh_select = st.sidebar.radio(
    label = 'Presence of the Rh factor in recipient\'s red blood cells:',
    options = ['Yes', 'No']
)
if (rh_select=="Yes"):
    input_df.loc[0,"RecipientRh"] = 1
else:
    input_df.loc[0,"RecipientRh"] = 0

st.sidebar.subheader('Risk Group')
risk = st.sidebar.radio(
    label = 'Risk Level:',
    options = ['High', 'Low']
)
if (risk=="High"):
    input_df.loc[0,"Riskgroup"] = 1
else:
    input_df.loc[0,"Riskgroup"] = 0

st.sidebar.subheader('Disease Group')
disease_group = st.sidebar.radio(
    label = 'Type of disease:',
    options = ['Malignant', 'Non-malignant']
)
if (disease_group=="Malignant"):
    input_df.loc[0,"Diseasegroup"] = 1
else:
    input_df.loc[0,"Diseasegroup"] = 0

st.sidebar.subheader('Disease')
disease_select = st.sidebar.selectbox(
    label = 'Disease Type',
    options = ['ALL', 'AML', 'Chronic', 'Lymphoma', 'Non-malignant']
)

if (disease_select=="ALL"):
    input_df.loc[0, "Disease_ALL"] = 1
elif (disease_select=="AML"):
    input_df.loc[0, "Disease_AML"] = 1
elif (disease_select=="Chronic"):
    input_df.loc[0, "Disease_chronic"] = 1
elif (disease_select=="Lymphoma"):
    input_df.loc[0, "Disease_lymphoma"] = 1
else:
    input_df.loc[0, "Disease_nonmalignant"] = 1

st.sidebar.markdown("# Input Transplant Donor Data")

st.sidebar.subheader('Stem Cell Source')
stem_select = st.sidebar.radio(
    label = 'Source of hematopoietic stem cells:',
    options = ['Peripheral Blood', 'Bone Marrow']
)
if (stem_select=="Peripheral Blood"):
    input_df.loc[0,"Stemcellsource"] = 1
else:
    input_df.loc[0,"Stemcellsource"] = 0

st.sidebar.subheader('Donor Age')
d_age = st.sidebar.number_input(
    label='Enter Donor Age (yrs):', min_value=0.0, max_value=150.0, value=45.0, step=0.1)
d_age = float(d_age)
d_age =(d_age-33.32463)/8.107825
input_df.loc[0,"Donorage"] = d_age
# input_df.iloc[0, input_df.columns.get_loc("Donorage")] = d_age

st.sidebar.subheader('Gender Match')
gender_match = st.sidebar.radio(
    label = 'Compatibility of the donor and recipient according to their gender:',
    options = ['Yes', 'No']
)
if (gender_match=="No"):
    input_df.loc[0,"Gendermatch"] = 1
else:
    input_df.loc[0,"Gendermatch"] = 0

st.sidebar.subheader('ABO Match')
abo_select = st.sidebar.radio(
    label = 'Compatibility of the donor and the recipient of hematopoietic stem cells according to ABO blood group:',
    options = ['Yes', 'No']
)
if (abo_select=="Yes"):
    input_df.loc[0,"ABOmatch"] = 1
else:
    input_df.loc[0,"ABOmatch"] = 0

st.sidebar.subheader('CMV Status')
cmv_status = st.sidebar.slider(
    'Serological compatibility of the donor and the recipient of hematopoietic stem cells according to cytomegalovirus infection prior to transplantation (the higher the value the lower the compatibility):',
    0, 3, 3)
input_df.loc[0,"CMVstatus"] = cmv_status

st.sidebar.subheader('Donor CMV')
donor_cmv = st.sidebar.radio(
    label = 'Presence of cytomegalovirus infection in the donor of hematopoietic stem cells prior to transplantation:',
    options = ['Yes', 'No']
)
if (donor_cmv=="Yes"):
    input_df.loc[0,"DonorCMV"] = 1
else:
    input_df.loc[0,"DonorCMV"] = 0

st.sidebar.subheader('Recipient CMV')
r_cmv = st.sidebar.radio(
    label = 'Presence of cytomegalovirus infection in the recipient of hematopoietic stem cells:',
    options = ['Yes', 'No']
)
if (r_cmv=="Yes"):
    input_df.loc[0,"RecipientCMV"] = 1
else:
    input_df.loc[0,"RecipientCMV"] = 0

st.sidebar.subheader('HLA Match')
hla_match = st.sidebar.radio(
    label = 'Compatibility of antigens of the main histocompatibility complex of the donor and the recipient of hematopoietic stem cells according to ALL international BFM SCT 2008 criteria:',
    options = ['10/10', '9/10', '8/10', '7/10']
)
if (hla_match=="10/10"):
    input_df.loc[0,"HLAmatch"] = 0
elif(hla_match=="9/10"):
    input_df.loc[0,"HLAmatch"] = 1
elif(hla_match=="8/10"):
    input_df.loc[0,"HLAmatch"] = 2
else:
    input_df.loc[0,"HLAmatch"] = 3

st.sidebar.subheader('HLA Mismatch')
mismatch = st.sidebar.radio(
    label = 'HLA match or mismatch between recipient and donor:',
    options = ['HLA matched', 'HLA mismatched']
)
if (mismatch=="HLA matched"):
    input_df.loc[0,"HLAmismatch"] = 0
else:
    input_df.loc[0,"HLAmismatch"] = 1

st.sidebar.subheader('Antigen')
antigen = st.sidebar.slider(
    'In how many antigens are different between the donor and the recipient:',
    0, 3, 3)
input_df.loc[0,"Antigen"] = antigen - 1

st.sidebar.subheader('Allele')
allele = st.sidebar.slider(
    'In how many alleles are different between the donor and the recipient:',
    0, 4, 3)
input_df.loc[0,"Alel"] = allele - 1


#############################################

st.markdown("### Model Prediction")

model = pickle.load(open("logistic_model.pickle",'rb'))
#st.write(model)

st.write(input_df)

output = model.predict(input_df)

button_clicked = st.button("Predict")

percent = round((model.predict_proba(input_df)[0][0])*100,2)
if (button_clicked):
        if percent <25:
            st.markdown(f"### Chance of survival is: **:red[{percent}%]**")
            st.write("##### :red[Chance of survival is low as patient is high risk.]")
        if percent >=25 and percent< 55:
            st.markdown(f"### Chance of survival is: **:orange[{percent}%]**")
            st.write("##### :orange[Patient has medium risk.]")
        if percent >=55:
            st.markdown(f"### Chance of survival is: **:green[{percent}%]**")
            st.write("##### :green[Patient is low risk, chance of survival is high.]")
        if percent >=80:
            st.markdown(f"### Chance of survival is: **:green[{percent}%]**")
            st.write("##### :green[Patient has very low risk. Chance of survival is very high.]")

        # st.write("Chance of survival is")
        # st.write(percent, "%")

        st.markdown("""---""")

        st.markdown("### High Risk Factors")
        if stem_select == 'Bone Marrow':
            st.write("- The patient received stem cells sourced from the **:red[bone marrow]** which could lead to higher rates of relapse")
        if (rh_select=="Yes"):
            st.write("- The patient has **:red[Rh factor]** in red blood cells which decreases survival probability.")
        if (cmv_status>1):
            st.write("- The patient has **:red[low serological compatibility of hematopoietic stem cells between donor and recipient]** which decreases survival probability.")
        if (disease_group=="Malignant"):
            st.write("- The patient has a **:red[malignant disease]** which decreases survival probability.")
        if (allele >= 2):
            st.write("- The patient has a **:red[higher number of differing alleles from the donor]** which decreases survival probability.")
        if (disease_select=="Lymphoma"):
            st.write("- The patient has **:red[Lymphoma]** which *sigificantly* decreases survival probability.")
        st.write("- **:green[Lower patient body mass]** correlates to higher survivability while **:red[higher patient body mass]** correlates to lower survivability.")
        fig, ax = plt.subplots()
        ax.hist(original_df["Rbodymass"], bins=20, alpha=0.5)
        if (r_mass > original_df["Rbodymass"].mean()):
            plt.axvline(x=r_mass, color= 'red', linewidth=2,)
        else:
            plt.axvline(x=r_mass, color= 'green', linewidth=2,)
        plt.suptitle("Distribution of Recipient Weights")

        st.pyplot(fig)

#############################################

enc = OrdinalEncoder()

