def simple_request():
    return {
        "messageVersion": "1.0",
        "invocationSource": "DialogCodeHook",
        "userId": "John",
        "bot": {
            "name": "BookTrip",
            "aliasId": "$LATEST",
            "version": "$LATEST"
        },
        "outputDialogMode": "Text",
        "sessionState": {
            "sessionAttributes": {},
            "intent": {
                "name": "BookHotel",
                "slots": {
                    "Location": {
                        "value":
                        {
                            "interpretedValue": "Chicago"
                        }
                    },
                    "CheckInDate": {
                        "value":
                        {
                            "interpretedValue": "2030-11-08"
                        }
                    },
                    "Nights": {
                        "value":
                        {
                            "interpretedValue": 4
                        }
                    },
                    "RoomType": {
                        "value":
                        {
                            "interpretedValue": "queen"
                        }
                    },
                    "breakfastIncluded": {
                        "value":
                        {
                            "interpretedValue": "Yes"
                        }
                    }
                },
                "confirmationStatus": "None"
            }
        }
    }


# TODO: Fill in with more relevant data
def full_request():
    return {
        "messageVersion": "1.0",
        "invocationSource": "DialogCodeHook",
        "inputMode": "Text",
        "responseContentType": "PlainText",
        "sessionId": "string",
        "inputTranscript": "string",
        "invocationLabel": "string",
        "bot": {
            "id": "string",
            "name": "BookTrip",
            "aliasId": "$LATEST",
            "localeId": "string",
            "version": "string"
        },
        "interpretations": [
            {
                "intent": {
                    "confirmationState": "None",
                    "name": "string",
                    "slots": {
                        "string": {
                            "value": {
                                "interpretedValue": "string",
                                "originalValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            }
                        },
                        "string": {
                            "shape": "List",
                            "value": {
                                "interpretedValue": "string",
                                "originalValue": "string",
                                "resolvedValues": [
                                    "string"
                                ]
                            },
                            "values": [
                                {
                                    "shape": "Scalar",
                                    "value": {
                                        "originalValue": "string",
                                        "interpretedValue": "string",
                                        "resolvedValues": [
                                            "string"
                                        ]
                                    }
                                },
                                {
                                    "shape": "Scalar",
                                    "value": {
                                        "originalValue": "string",
                                        "interpretedValue": "string",
                                        "resolvedValues": [
                                            "string"
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    "state": "Failed | Fulfilled | FulfillmentInProgress | InProgress | ReadyForFulfillment | Waiting",
                    "kendraResponse": {
                        # Only present when intent is KendraSearchIntent. For details, see
                        # https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html#API_Query_ResponseSyntax
                    }
                },
                "nluConfidence": 1,
                "sentimentResponse": {
                    "sentiment": "string",
                    "sentimentScore": {
                        "mixed": 1,
                        "negative": 1,
                        "neutral": 1,
                        "positive": 1
                    }
                }
            }
        ],
        "proposedNextState": {
            "dialogAction": {
                "slotToElicit": "string",
                "type": "Close | ConfirmIntent | Delegate | ElicitIntent | ElicitSlot"
            },
            "intent": {
                "name": "string",
                "confirmationState": "Confirmed | Denied | None",
                "slots": {},
                "state": "Failed | Fulfilled | InProgress | ReadyForFulfillment | Waiting"
            },
            "prompt": {
                "attempt": "string"
            }
        },
        "requestAttributes": {
            "string": "string"
        },
        "sessionState": {
            "activeContexts": [
                {
                    "name": "string",
                    "contextAttributes": {
                        "string": "string"
                    },
                    "timeToLive": {
                        "timeToLiveInSeconds": 60,
                        "turnsToLive": 20
                    }
                }
            ],
            "sessionAttributes": {
                "string": "string"
            },
            "runtimeHints": {
                "slotHints": {
                    "string": {
                        "string": {
                            "runtimeHintValues": [
                                {
                                    "phrase": "string"
                                },
                                {
                                    "phrase": "string"
                                }
                            ]
                        }
                    }
                }
            },
            "dialogAction": {
                "slotToElicit": "string",
                "type": "Close | ConfirmIntent | Delegate | ElicitIntent | ElicitSlot"
            },
            "intent": {
                "confirmationState": "Confirmed | Denied | None",
                "name": "string",
                "slots": {
                    "string": {
                        "value": {
                            "interpretedValue": "string",
                            "originalValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        }
                    },
                    "string": {
                        "shape": "List",
                        "value": {
                            "interpretedValue": "string",
                            "originalValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        },
                        "values": [
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "interpretedValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            },
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "interpretedValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            }
                        ]
                    }
                },
                "state": "Failed | Fulfilled | FulfillmentInProgress | InProgress | ReadyForFulfillment | Waiting",
                "kendraResponse": {
                    # Only present when intent is KendraSearchIntent. For details, see
                    # https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html#API_Query_ResponseSyntax
                },
                "originatingRequestId": "string"
            }
        },
        "transcriptions": [
            {
                "transcription": "string",
                "transcriptionConfidence": 1,
                "resolvedContext": {
                    "intent": "string"
                },
                "resolvedSlots": {
                    "string": {
                        "shape": "List",
                        "value": {
                            "originalValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        },
                        "values": [
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            },
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            }
                        ]
                    }
                }
            }
        ]
    }


def simple_result():
    return {
        "sessionState": {
            "sessionAttributes": {
                "string": "string"
            },
            "runtimeHints": {
                "slotHints": {
                    "string": {
                        "string": {
                            "runtimeHintValues": [
                                {
                                    "phrase": "string"
                                },
                                {
                                    "phrase": "string"
                                }
                            ]
                        }
                    }
                }
            },
            "dialogAction": {
                "slotToElicit": "string",
                "type": "ElicitSlot"
            },
            "intent": {
                "confirmationState": "None",
                "name": "BookHotel",
                "slots": {
                    "Location": {
                        "interpretedValue": "Chicago"
                    },
                    "CheckInDate": {
                        "interpretedValue": "2030-11-08"
                    },
                    "Nights": {
                        "interpretedValue": 4
                    },
                    "RoomType": {
                        "interpretedValue": "queen"
                    }
                },
                "state": "InProgress"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "test message"
            }
        ]
    }


# TODO: Fill in with more relevant data
def full_result():
    return {
        "sessionState": {
            "activeContexts": [
                {
                    "name": "string",
                    "contextAttributes": {
                        "key": "value"
                    },
                    "timeToLive": {
                        "timeToLiveInSeconds": 60,
                        "turnsToLive": 20
                    }
                }
            ],
            "sessionAttributes": {
                "string": "string"
            },
            "runtimeHints": {
                "slotHints": {
                    "string": {
                        "string": {
                            "runtimeHintValues": [
                                {
                                    "phrase": "string"
                                },
                                {
                                    "phrase": "string"
                                }
                            ]
                        }
                    }
                }
            },
            "dialogAction": {
                "slotElicitationStyle": "Default | SpellByLetter | SpellByWord",
                "slotToElicit": "string",
                "type": "Close | ConfirmIntent | Delegate | ElicitIntent | ElicitSlot"
            },
            "intent": {
                "confirmationState": "Confirmed | Denied | None",
                "name": "string",
                "slots": {
                    "string": {
                        "value": {
                            "interpretedValue": "string",
                            "originalValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        }
                    },
                    "string": {
                        "shape": "List",
                        "value": {
                            "originalValue": "string",
                            "interpretedValue": "string",
                            "resolvedValues": [
                                "string"
                            ]
                        },
                        "values": [
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "interpretedValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            },
                            {
                                "shape": "Scalar",
                                "value": {
                                    "originalValue": "string",
                                    "interpretedValue": "string",
                                    "resolvedValues": [
                                        "string"
                                    ]
                                }
                            }
                        ]
                    }
                },
                "state": "Failed | Fulfilled | FulfillmentInProgress | InProgress | ReadyForFulfillment | Waiting"
            }
        },
        "messages": [
            {
                "contentType": "CustomPayload | ImageResponseCard | PlainText | SSML",
                "content": "string",
                "imageResponseCard": {
                    "title": "string",
                    "subtitle": "string",
                    "imageUrl": "string",
                    "buttons": [
                        {
                            "text": "string",
                            "value": "string"
                        }
                    ]
                }
            }
        ],
        "requestAttributes": {
            "string": "string"
        }
    }
