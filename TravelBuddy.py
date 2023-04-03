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

    match intent_name:
        case "BookFlight":
            result = book_flight.process(event)
        case "BookCar":
            result = book_car.process(event)
        case "BookHotel":
            result = book_hotel.process(event)
        case _:
            raise Exception('No environment variable for intent: ' + intent_name)

    print(result)
    payload = json.load(result)
    return payload


# Entry point
def lambda_handler(event, context):
    print(event)
    response = router(event)
    return response
