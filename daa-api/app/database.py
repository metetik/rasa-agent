from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from app.config import get_database_url
from app.models import Staff, Patient, Agent, TreatmentPlan, Treatment, PaymentPlan, Payment, Image, Notification, TreatmentNotes
from datetime import datetime, timedelta


DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def populate_tables():
    # TODO: Create appointment
    try:
        with Session(engine) as session:
            # Create staff members
            staff1 = Staff(first_name="Olivia", last_name="Jones", role="Dentist")
            staff2 = Staff(first_name="Ethan", last_name="Brown", role="Assistant")
            staff3 = Staff(first_name="William", last_name="White", role="Dentist")
            staff4 = Staff(first_name="Chloe", last_name="Taylor", role="Assistant")
            session.add_all([staff1, staff2, staff3, staff4])
            session.commit()

            # Create patients
            patient1 = Patient(
                identity_number="1234567890",
                first_name="Michael",
                last_name="Evans",
                age=30
            )
            patient2 = Patient(
                identity_number="9876543210",
                first_name="Grace",
                last_name="Thompson",
                age=45
            )
            session.add_all([patient1, patient2])
            session.commit()

            # Create an agent
            agent1 = Agent(name="AI Assistant", model="gemma3")
            session.add(agent1)
            session.commit()

            # Create a treatment plan
            treatment_plan1 = TreatmentPlan(
                patient_id=patient1.id,
                description="Comprehensive dental checkup",
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30),
                status="Active"
            )
            session.add(treatment_plan1)
            session.commit()

            # Create a treatment
            treatment1 = Treatment(
                treatment_plan_id=treatment_plan1.id,
                patient_id=patient1.id,
                dentist_id=staff1.id,
                agent_id=agent1.id,
                name="Dental Cleaning",
                description="Deep cleaning and cavity check",
                cost=200.0,
                status="Scheduled"
            )
            session.add(treatment1)
            session.commit()

            # Create a payment plan
            payment_plan1 = PaymentPlan(
                patient_id=patient1.id,
                created_by_id=staff1.id,
                total_amount=500.0,
                paid_amount=100.0,
                remaining_amount=400.0,
                status="Active",
                description="Regular checkup payment"
            )
            session.add(payment_plan1)
            session.commit()

            # Create a payment
            payment1 = Payment(
                payment_plan_id=payment_plan1.id,
                status="Completed",
                operation="Credit Card",
                amount=100.0
            )
            session.add(payment1)
            session.commit()

            # Create an image
            image1 = Image(
                patient_id=patient1.id,
                treatment_id=treatment1.id,
                url="https://example.com/image1.jpg",
                description="Initial X-ray"
            )
            session.add(image1)
            session.commit()

            # Create a notification
            notification1 = Notification(
                patient_id=patient1.id,
                staff_id=staff1.id,
                message="Your appointment is scheduled for tomorrow",
                read=False
            )
            session.add(notification1)
            session.commit()

            # Create treatment notes
            treatment_note1 = TreatmentNotes(
                treatment_id=treatment1.id,
                agent_id=agent1.id,
                content="Patient presented with mild gingivitis. Recommended improved brushing technique."
            )
            session.add(treatment_note1)
            session.commit()

            print("Tables populated with example data successfully.")
    except Exception as e:
        print(f"Error populating tables: {str(e)}")
        session.rollback()
        raise