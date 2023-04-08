import json
import boto3
import book_flight
import book_car
import book_hotel

# reuse client connection as global
client = boto3.client('lambda')


# Intent Router
def router(event):
    intent_name = event['sessionState']['intent']['name']
    print(f"Intent: {intent_name}")

    if intent_name == "BookFlight":
        flight_booking = book_flight.BookFlight(event)
        result = flight_booking.process()
    elif intent_name == "BookCar":
        car_booking = book_car.BookCar(event)
        result = car_booking.process()
    elif intent_name == "BookHotel":
        hotel_booking = book_hotel.BookHotel(event)
        result = hotel_booking.process()
    else:
        raise Exception('No environment variable for intent: ' + intent_name)
    # payload = json.load(result)
    return result


# Entry point
def lambda_handler(event, context):
    response = router(event)
    return response
