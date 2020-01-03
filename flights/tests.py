from django.test import Client, TestCase
from django.db.models import Max

from .models import Flight, Airport, Passenger

# Create your tests here.

class ModelTestCase(TestCase):
    
    # Model Test Cases:
    
    def setUp(self): 

        # Create Airports:
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create Flights:
        f1 = Flight.objects.create(origin=a1, destination=a2, duration=100)
        f2 = Flight.objects.create(origin=a1, destination=a1, duration=200)
        f3 = Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        """This test checks if departure count from particular airport is equal."""
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)
    
    def test_arrivals_count(self):
        """This test checks if arrival count from particular airport is equal."""
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)
    
    def test_valid_flight(self):
        """This test checks if flight is valid."""
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())
    
    def test_invalid_flight_destination(self):
        """This test checks if flight destination is invalid."""
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        """This test checks if flight duration is invalid."""
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())
    
    # Views Test Cases:
    
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)
    
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))['id__max']

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
    
    def test_flight_page_passenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Arya", last="Stark")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)
    
    def test_flight_page_non_passenger(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Tyrion", last="Lannister")
        
        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)

        