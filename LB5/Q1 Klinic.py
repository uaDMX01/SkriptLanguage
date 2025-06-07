import datetime

class Person:
    """Базовий клас для особи (пацієнта або лікаря)."""
    def __init__(self, id, name, contact_info):
        self.id = id
        self.name = name
        self.contact_info = contact_info # Наприклад, dict: {'phone': '...', 'email': '...'}

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Patient(Person):
    """Клас для пацієнтів1."""
    def __init__(self, id, name, contact_info, birth_date):
        super().__init__(id, name, contact_info)
        self.birth_date = birth_date
        self.medical_history = [] # Список об'єктів MedicalRecord

    def add_medical_record(self, record):
        if isinstance(record, MedicalRecord):
            self.medical_history.append(record)
        else:
            raise ValueError("Запис повинен бути об'єктом класу MedicalRecord.")

    def get_medical_history(self):
        return self.medical_history

class Doctor(Person):
    """Клас для лікарів."""
    def __init__(self, id, name, contact_info, specialization):
        super().__init__(id, name, contact_info)
        self.specialization = specialization
        self.appointments = [] # Список об'єктів Appointment

    def add_appointment(self, appointment):
        if isinstance(appointment, Appointment):
            self.appointments.append(appointment)
        else:
            raise ValueError("Запис на прийом повинен бути об'єктом класу Appointment.")

    def get_appointments(self):
        return self.appointments

class Appointment:
    """Клас для записів на прийом."""
    def __init__(self, appointment_id, patient, doctor, date_time, reason):
        self.appointment_id = appointment_id
        self.patient = patient        # Об'єкт Patient
        self.doctor = doctor          # Об'єкт Doctor
        self.date_time = date_time    # Об'єкт datetime.datetime
        self.reason = reason

    def __str__(self):
        return (f"Прийом ID: {self.appointment_id}, "
                f"Пацієнт: {self.patient.name}, "
                f"Лікар: {self.doctor.name}, "
                f"Дата/Час: {self.date_time.strftime('%Y-%m-%d %H:%M')}, "
                f"Причина: {self.reason}")

class MedicalRecord:
    """Клас для медичних історій."""
    def __init__(self, record_id, patient, doctor, date, diagnosis, treatment):
        self.record_id = record_id
        self.patient = patient       # Об'єкт Patient
        self.doctor = doctor         # Об'єкт Doctor
        self.date = date             # Об'єкт datetime.date
        self.diagnosis = diagnosis
        self.treatment = treatment

    def __str__(self):
        return (f"Медичний запис ID: {self.record_id}, "
                f"Пацієнт: {self.patient.name}, "
                f"Лікар: {self.doctor.name}, "
                f"Дата: {self.date.strftime('%Y-%m-%d')}, "
                f"Діагноз: {self.diagnosis}, "
                f"Лікування: {self.treatment}")

class Clinic:
    """Основний клас "Клініка"."""
    def __init__(self, name):
        self.name = name
        self.patients = {}  # dict: {patient_id: patient_object}
        self.doctors = {}   # dict: {doctor_id: doctor_object}
        self.appointments = {} # dict: {appointment_id: appointment_object}
        self.medical_records = {} # dict: {record_id: medical_record_object}
        self._next_appointment_id = 1
        self._next_medical_record_id = 1

    def add_patient(self, patient):
        if not isinstance(patient, Patient):
            raise ValueError("Об'єкт повинен бути екземпляром класу Patient.")
        if patient.id in self.patients:
            print(f"Пацієнт з ID {patient.id} вже існує.")
            return False
        self.patients[patient.id] = patient
        print(f"Пацієнт {patient.name} доданий.")
        return True

    def get_patient(self, patient_id):
        return self.patients.get(patient_id)

    def add_doctor(self, doctor):
        if not isinstance(doctor, Doctor):
            raise ValueError("Об'єкт повинен бути екземпляром класу Doctor.")
        if doctor.id in self.doctors:
            print(f"Лікар з ID {doctor.id} вже існує.")
            return False
        self.doctors[doctor.id] = doctor
        print(f"Лікар {doctor.name} доданий.")
        return True

    def get_doctor(self, doctor_id):
        return self.doctors.get(doctor_id)

    def schedule_appointment(self, patient_id, doctor_id, date_time_str, reason):
        patient = self.get_patient(patient_id)
        doctor = self.get_doctor(doctor_id)

        if not patient:
            print(f"Пацієнт з ID {patient_id} не знайдений.")
            return None
        if not doctor:
            print(f"Лікар з ID {doctor_id} не знайдений.")
            return None

        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
        except ValueError:
            print("Невірний формат дати/часу. Використовуйте 'РРРР-ММ-ДД ГГ:ХХ'.")
            return None

        appointment_id = self._next_appointment_id
        appointment = Appointment(appointment_id, patient, doctor, date_time_obj, reason)
        self.appointments[appointment_id] = appointment
        # patient.add_appointment(appointment) # ВИДАЛИТИ ЦЕЙ РЯДОК
        doctor.add_appointment(appointment) # ЦЕЙ РЯДОК ПОВИНЕН БУТИ
        self._next_appointment_id += 1
        print(f"Запис на прийом ID {appointment_id} створено.")
        return appointment

    def add_medical_record_to_patient(self, patient_id, doctor_id, date_str, diagnosis, treatment):
        patient = self.get_patient(patient_id)
        doctor = self.get_doctor(doctor_id)

        if not patient:
            print(f"Пацієнт з ID {patient_id} не знайдений.")
            return None
        if not doctor:
            print(f"Лікар з ID {doctor_id} не знайдений.")
            return None

        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Невірний формат дати. Використовуйте 'РРРР-ММ-ДД'.")
            return None

        record_id = self._next_medical_record_id
        record = MedicalRecord(record_id, patient, doctor, date_obj, diagnosis, treatment)
        self.medical_records[record_id] = record
        patient.add_medical_record(record)
        self._next_medical_record_id += 1
        print(f"Медичний запис ID {record_id} додано для пацієнта {patient.name}.")
        return record

    def get_patient_medical_history(self, patient_id):
        patient = self.get_patient(patient_id)
        if patient:
            return patient.get_medical_history()
        return []

    def get_doctor_appointments(self, doctor_id):
        doctor = self.get_doctor(doctor_id)
        if doctor:
            return doctor.get_appointments()
        return []

# --- Приклад використання класу "Клініка" ---
if __name__ == "__main__":
    my_clinic = Clinic("Моя Добробут Клініка")

    # Додавання пацієнтів
    patient1 = Patient(1, "Іванов Іван", {'phone': '0981112233', 'email': 'ivanov@example.com'}, datetime.date(1990, 5, 15))
    patient2 = Patient(2, "Петрова Анна", {'phone': '0674445566', 'email': 'petrova@example.com'}, datetime.date(1985, 10, 20))

    my_clinic.add_patient(patient1)
    my_clinic.add_patient(patient2)

    # Додавання лікарів
    doctor1 = Doctor(101, "Ковальчук Олена", {'phone': '0507778899', 'email': 'kovalchuk@example.com'}, "Терапевт")
    doctor2 = Doctor(102, "Мельник Сергій", {'phone': '0631112233', 'email': 'melnyk@example.com'}, "Хірург")

    my_clinic.add_doctor(doctor1)
    my_clinic.add_doctor(doctor2)

    print("\n--- Записи на прийом ---")
    # Запис на прийом
    app1 = my_clinic.schedule_appointment(1, 101, "2025-06-10 10:00", "Загальний огляд")
    app2 = my_clinic.schedule_appointment(2, 101, "2025-06-10 11:00", "Консультація")
    app3 = my_clinic.schedule_appointment(1, 102, "2025-06-11 14:30", "Післяопераційний огляд")

    if app1: print(app1)
    if app2: print(app2)
    if app3: print(app3)

    print("\n--- Медичні історії ---")
    # Додавання медичних записів
    rec1 = my_clinic.add_medical_record_to_patient(1, 101, "2025-06-10", "ГРВІ", "Антибіотики, постільний режим")
    rec2 = my_clinic.add_medical_record_to_patient(2, 101, "2025-06-10", "Головний біль", "Парацетамол")
    rec3 = my_clinic.add_medical_record_to_patient(1, 102, "2025-06-11", "Стан після операції", "Перев'язка, спостереження")

    if rec1: print(rec1)
    if rec2: print(rec2)
    if rec3: print(rec3)

    print("\n--- Перегляд даних ---")
    # Перегляд медичної історії пацієнта
    print(f"\nМедична історія для {patient1.name}:")
    for record in my_clinic.get_patient_medical_history(1):
        print(f"- {record.date}: {record.diagnosis} - {record.treatment}")

    # Перегляд прийомів лікаря
    print(f"\nПрийоми для {doctor1.name}:")
    for appointment in my_clinic.get_doctor_appointments(101):
        print(f"- {appointment.date_time.strftime('%Y-%m-%d %H:%M')}: Пацієнт {appointment.patient.name}, Причина: {appointment.reason}")