import names
import random
import json
import pandas as pd
import numpy as np
from faker import Faker
import datetime
from datetime import date
from Postgres_Class import CustomPostgresClass

# print(names.get_full_name())
fake = Faker()
patient_data = []
doctor_data = []
staff_data = []

####Patient's Data
for j in range(100):
    gender = np.random.choice(["Male", "Female"], p=[0.5, 0.5])
    address = fake.address().splitlines()
    has_insurance = fake.boolean(chance_of_getting_true=75)
    patient_data += [{
                # 'pid' : uuid.uuid4(),
                "name": fake.name_male() if gender=="Male" else fake.name_female(),
                "gender": str(gender),
                # "LastName": fake.last_name(),
                'dob':fake.date_of_birth(),
                'address_line1' : address[0],
                'city': address[1][:-10],
                'country':address[1][-8:-6],
                'zipcode':address[1][-5:],
                'phoneno':fake.phone_number(),
                'email' : fake.email(),
                'has_insurance': has_insurance,
                'insurance_no': random.randint(1, 1000) if has_insurance==True else 'NULL',
                'is_active': fake.boolean(chance_of_getting_true=75)
               }]
df = pd.DataFrame(patient_data)
df.insert(0, 'patient_id', range(1, 1 + len(df)))

patient_data = df.to_dict('records')
# with open('patient_data.json','w') as f:
#     my_dict = json.dump(a,f,indent=2)
 


####Patient_logs, payments and insurance data

patient_logs = []
payments = []
insurance_data = []
today = date.today()
payment_method = ['Cash','Card']
for i in range(0,len(patient_data)):
    if patient_data[i]['is_active'] == False:
        patient_logs += [{
                       'patient_id': patient_data[i]['patient_id'],
                       'date':date.today(),
                       'day_of_admission':date.today().strftime("%A"),
                       'current_diagnosis_id':random.randint(1, 10),
                       'assigned_doctor_id':random.randint(1, 100),
                       'amount_received': 10000,
                       }]
 
        
for i in range(0,len(patient_data)):
    if patient_data[i]['is_active'] == False and patient_data[i]['has_insurance'] == False:  
        cost_of_stay = random.randint(1000, 10000)
        drug_cost = random.randint(100, 5000)
        amount_due = fake.boolean(chance_of_getting_true=25)
        payments += [{
                       'patient_id': patient_data[i]['patient_id'],
                       'payment_method':random.choice(payment_method),
                       'cost_of_stay':cost_of_stay,
                       'drug_cost':drug_cost,
                       'amount_due':amount_due,
                       'date_of_bill_paid':date.today() if amount_due==False else 'NULL',
                       }]
        
    elif patient_data[i]['is_active'] == False and patient_data[i]['has_insurance'] == True:
        cost_of_stay = random.randint(1000, 10000)
        drug_cost = random.randint(100, 5000)
        payments += [{
                       'patient_id': patient_data[i]['patient_id'],
                       'payment_method':'Insurance',
                       'cost_of_stay':cost_of_stay,
                       'drug_cost':drug_cost,
                       'amount_due':amount_due,
                       'date_of_bill_paid':date.today() if amount_due==False else 'NULL',
                       }]
        
        insurance_type = ['individual','joint']
        age = today.year - patient_data[i]['dob'].year - ((today.month, today.day) < (patient_data[i]['dob'].month, patient_data[i]['dob'].day))
        insurance_data += [{
                       'issuer_id': patient_data[i]['patient_id'],
                       'insurance_no':patient_data[i]['insurance_no'],
                       'claim_amount':cost_of_stay, 
                       'insurance_type':random.choice(insurance_type),
                       'holding_policy_duration':random.randint(0,age),
                       'dob':patient_data[i]['dob'],
                       'city':patient_data[i]['city'],
                       'country':patient_data[i]['country'],
                       'zipcode':patient_data[i]['zipcode']
                       }]

    
####Doctor's Data    
for j in range(50):
    gender = np.random.choice(["Male", "Female"], p=[0.5, 0.5])
    address = fake.address().splitlines()
    doctor_data += [{
                # 'pid' : uuid.uuid4(),
                "name": fake.name_male() if gender=="Male" else fake.name_female(),
                "gender": str(gender),
                # "LastName": fake.last_name(),
                'dob':fake.date_of_birth().strftime("%d-%m-%Y"),
                'address_line1' : address[0],
                'city': address[1][:-10],
                'country':address[1][-8:-6],
                'zipcode':address[1][-5:],
                'phoneno':fake.phone_number(),
                'email' : fake.email(),
                
               }]
df = pd.DataFrame(doctor_data)
df.insert(0, 'doctor_id', range(1, 1 + len(df)))

doctor_data = df.to_dict('records')
# with open('doctor_data.json','w') as f:
#     my_dict = json.dump(b,f,indent=2)
    
####Staff Data   
staff = ['Nurse', 'Physician', 'Assistants', 'Pharmacist', 'Therapist'] 
for j in range(300):
    gender = np.random.choice(["Male", "Female"], p=[0.5, 0.5])
    address = fake.address().splitlines()
    staff_data += [{
                # 'pid' : uuid.uuid4(),
                'category':random.choice(staff),
                "name": fake.name_male() if gender=="Male" else fake.name_female(),
                "gender": str(gender),
                # "LastName": fake.last_name(),
                'dob':fake.date_of_birth().strftime("%d-%m-%Y"),
                'address_line1' : address[0],
                'city': address[1][:-10],
                'country':address[1][-8:-6],
                'zipcode':address[1][-5:],
                'phoneno':fake.phone_number(),
                'email' : fake.email(),  
               }]
staff_df = pd.DataFrame(staff_data)
staff_df.insert(0, 'staff_id', range(1, 1 + len(staff_df)))

staff_data = staff_df.to_dict('records')


####Beds data

beds_data = []

for i in range(300):
    beds_data +=[{
                'bed_id':random.randint(1, 100),
                'room_id':random.randint(1, 50),
                'floor_id':random.randint(1, 5)
                }]
    
    
    
####Diagnosis data
diagnosis = []
count = 0
names = ['Bypass','Cardiac Arrest', 'Chemotherapy', 'Chronic Headache','Diabetes','Ear Infection','EKG', 'Epilepsy','Hypoglycemia','Radiotherapy']

for name in names: 
    count = count + 1
    diagnosis +=[{
                'id': count,
                'name': name
                }]


####Admissions Data
admission_data = []
end = random.randint(1, len(patient_data))
for i in range(end):

    admission_data += [{
                   'patient_id': random.randint(1, end),
                   'admission_date':date.today(),
                   'bed_id':random.randint(1, 100),
                   }]   




obj = CustomPostgresClass('truthics.com','testing','datasync','24EvNRMuZ845VHm5')
obj.insert_data_into_table('healthcare_data.patients', patient_data)
obj.insert_data_into_table('healthcare_data.patient_log', patient_logs)
obj.insert_data_into_table('healthcare_data.admissions', admission_data)
obj.insert_data_into_table('healthcare_data.payments', payments)
obj.insert_data_into_table('healthcare_data.insurance', insurance_data)
obj.insert_data_into_table('healthcare_data.staff', staff_data)
obj.insert_data_into_table('healthcare_data.beds', beds_data)
obj.insert_data_into_table('healthcare_data.doctors', doctor_data)
obj.insert_data_into_table('healthcare_data.diagnosis', diagnosis)

