from unittest import TestCase

from index import analyseMessage

message = {
    "teamId": "black-543",
    "event": "xxxxx",
    "droneInfo": {
        "location": {
            "latitude": 48.86439099043799,
            "longitude": 2.3426746801338623
        },
        "topicUrl": "https://europe-west1-...",
        "parcels": [
            {
                "teamId": "black-543",
                "status": "AVAILABLE",
                "location": {
                    "pickup": {
                        "latitude": 48.90524759169551,
                        "longitude": 2.2657060097635626
                    },
                    "delivery": {
                        "latitude": 48.867271697034234,
                        "longitude": 5.273857921355812
                    }
                },
                "type": "CLASSIC",
                "score": 50
            },
        ],
        "score": 0
    },
    "availableParcelsForTeam": [
        {
            "teamId": "black-543",
            "status": "AVAILABLE",
            "location": {
                "pickup": {
                    "latitude": 46.90524759169551,
                    "longitude": 52.2657060097635626
                },
                "delivery": {
                    "latitude": 48.867271697034234,
                    "longitude": 2.273857921355812
                }
            },
            "type": "CLASSIC",
            "score": 50
        },
        {
            "teamId": "black-543",
            "status": "AVAILABLE",
            "location": {
                "pickup": {
                    "latitude": 48.90524759169551,
                    "longitude": 2.2657060097635626
                }
            },
            "type": "SPEED_BOOST",
            "score": 0.1
        }
    ]
}


class TestMoving(TestCase):

    def test_receiving_waiting_for_command(self):
        # Given
        localMessage = message
        localMessage["event"] = "WAITING_FOR_COMMAND"

        # When
        result = analyseMessage(localMessage)

        # Then
        self.assertEqual("black-543", result["teamId"])
        self.assertEqual("MOVE", result["command"]["name"])
        self.assertEqual(48.867271697034234, result["command"]["location"]["latitude"])
        self.assertEqual(5.273857921355812, result["command"]["location"]["longitude"])

    def test_receiving_waiting_for_command(self):
        # Given
        localMessage = message
        localMessage["event"] = "WAITING_FOR_COMMAND"
        localMessage["droneInfo"]["parcels"] = {}

        # When
        result = analyseMessage(localMessage)

        # Then
        self.assertEqual("black-543", result["teamId"])
        self.assertEqual("MOVE", result["command"]["name"])
        self.assertEqual(46.90524759169551, result["command"]["location"]["latitude"])
        self.assertEqual(52.2657060097635626, result["command"]["location"]["longitude"])

    def test_receiving_moving(self):
        # Given
        localMessage = message
        localMessage["event"] = "MOVING"

        # When
        result = analyseMessage(localMessage)

        # Then
        self.assertEqual(None, result)

    def test_receiving_move_location_error(self):
        # Given
        localMessage = message
        localMessage["event"] = "MOVE_LOCATION_ERROR"

        # When
        result = analyseMessage(localMessage)

        # Then
        self.assertEqual(None, result)
