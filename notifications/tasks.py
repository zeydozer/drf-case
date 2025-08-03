from celery import shared_task

@shared_task
def send_flight_delay_notification(flight_id, flight_number):
    print(f"🚨 Uyarı: {flight_number} (ID: {flight_id}) uçuşu gecikmiştir.")
