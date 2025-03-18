**Task:** Generate a `models.py` file for the FastAPI backend of a chatbot application being developed with Rasa.

**Context:**

* The chatbot application's core architecture is Rasa.
* The backend API will be developed using FastAPI.
* SQLModel will be used for database interaction.

**Input:**

Below is the application's requirements document and a list of SQLModel models to be used.  Use this information to create the `models.py` file.

Requirements Document: 
```markdown
# Requirements for the Dental Assistant Agent

**Problem Definition:** Dental assistant staff in small and medium-sized clinics often juggle a wide range of responsibilities, from patient treatment tasks to managing appointments and retrieving patient information. This heavy workload can be challenging for the assistant and reduces efficiency. The purpose of the Dental Assistant Agent is to simplify and accelerate these processes for both the assistant and the dentist, thereby reducing the workload for both and creating a more efficient working environment.

## Requirements

- **New Patient Record Creation:** The Agent should be able to create a new patient record.
- **Appointment Scheduling:** The Agent should be able to schedule new appointments for patients.
- **Appointment Notifications:** The Agent should be able to send appointment notifications to patients via email or SMS.
- **Treatment History Inquiry:** The Agent should be able to retrieve a patient’s treatment history.
- **Patient Information Inquiry:** The Agent should be able to retrieve a patient’s personal and treatment information.
- **Treatment Plan Recording:** The Agent should be able to record a treatment plan for a patient.
- **Treatment Plan Notifications:** The Agent should be able to send the patient-specific treatment plan to the patient as a notification.
- **Treatment Suggestions:** The Agent should be able to provide treatment suggestions based on technical information received from the dentist.
- **Image Analysis:** The Agent should be able to direct images (typically X-rays) received from the dentist to an image analysis model to perform the analyses expected by the dentist.
- **Treatment Completion Notifications:** The Agent should be able to send a notification to the patient detailing the procedures performed and the payment plan.
- **Delay Notifications:** The Agent should be able to send a notification to the patient if there is a delay in their scheduled appointment.
- **Upcoming Appointment Reminders:** The Agent should be able to send reminder notifications to patients about their upcoming appointments.
```

SQLModel List
```markdown
- Staff
	- Id
	- Name
	- Surname
	- Role 
	- ...

- Patient
	- Id
	- IdentityNumber
	- Name
	- Surname
	- Age
	- Notes
	- ...

- PatientNote
	- Id
	- Patient
	- CreateDate
	- ModifiedDate
	- Content
	- ...

- Appointment
	- Id
	- Patient
	- Dentist
	- Description
	- StartDate
	- EndDate
	- Completed
	- ...

- Agent
	- Id
	- Name
	- Model
	- ...

- TreatmentPlan
	- Id
	- Patient
	- Treatments
	- CreatedByDentist
	- CreatedDate
	- ModifiedDate
	- Agent
	- ...

- Treatment
	- Id
	- TreatmentPlan
	- Patient
	- Dentist
	- Agent
	- TreatmentNotes
	- Status
	- ModifiedDate
	- ...


- TreatmentNotes
	- Id
	- Treatment
	- Content
	- CreatedDate
	- ModifiedDate
	- Agent
	- ...

- PaymentPlan
	- Id
	- Patient
	- Description
	- CreatedBy
	- CreatedDate
	- ModifiedDate
	- Payments
	- ...

- Payment
	- Id
	- Status
	- Operation
	- Amount
	- Description
	- ...

- Image
	- Id
	- Name
	- Patient
	- CreatedBy
	- CreatedDate
	- ModifiedDate
	- ImageContent
	- ImageLink
	- Description
	- ...

- Notification
	- Id
	- NotificationType
	- Content
	- SendDate
	- ...
```

**Output:**

* The contents of the `models.py` file.
* The file should contain relational database models defined using the SQLModel library.
* Relationships between models should be defined correctly and necessary features like `back_populates` should be utilized.
* The code should adhere to Python best practices, be readable, and maintainable.
* Include brief comments explaining the purpose and important fields of each model.

**Additional Information (Optional):**

* The database system to be used (e.g., SQLite, PostgreSQL, MySQL)
* Additional details about the complexity of model relationships
* Any specific requirements or constraints
