from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Munro, ClimbRecord, UserFavouriteMunro, UserProfile
from datetime import date


class ModelTests(TestCase):
    def test_munro_str(self):
        m = Munro.objects.create(name="Ben Nevis", height=1345, location="Fort William", region="Highlands", difficulty_rating=5, description="Highest")
        self.assertEqual(str(m), "Ben Nevis")

    def test_climbrecord_str(self):
        User = get_user_model()
        user = User.objects.create_user(username="alice", password="pass12345")
        m = Munro.objects.create(name="Schiehallion", height=1083, location="Perthshire", region="Highlands", difficulty_rating=3, description="Cone")
        r = ClimbRecord.objects.create(user=user, munro=m, climb_date=date(2024, 1, 1), total_meters_climbed=900, total_distance=10, completion_time_hours=5, star_rating=4)
        self.assertIn("alice", str(r))
        self.assertIn("Schiehallion", str(r))

    def test_user_favourite_str(self):
        User = get_user_model()
        user = User.objects.create_user(username="bob", password="pass12345")
        m = Munro.objects.create(name="Ben Lomond", height=974, location="Loch Lomond", region="Central", difficulty_rating=2, description="Popular")
        fav = UserFavouriteMunro.objects.create(user=user, munro=m)
        self.assertIn("bob", str(fav))
        self.assertIn("Ben Lomond", str(fav))


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", email="t@e.com", password="pass12345")

    def test_index_ok(self):
        Munro.objects.create(name="Aonach Beag", height=1234, location="Lochaber", region="Highlands", difficulty_rating=4, description="Nice")
        url = reverse("munro_app:index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("top_munros", res.context)

    def test_munro_list_filters(self):
        Munro.objects.create(name="Ben Macdui", height=1309, location="Cairngorms", region="Highlands", difficulty_rating=4, description="Second")
        Munro.objects.create(name="Ben Vorlich", height=985, location="Perthshire", region="Central", difficulty_rating=2, description="Easy")
        url = reverse("munro_app:munro_list")
        res = self.client.get(url, {"region": "Highlands"})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(m.region == "Highlands" for m in res.context["munros"]))

    def test_add_climb_requires_login(self):
        m = Munro.objects.create(name="Stob Binnein", height=1165, location="Crianlarich", region="Central", difficulty_rating=3, description="Ridge")
        url = reverse("munro_app:add_climb")
        res = self.client.post(url, {"munro": m.id, "climb_date": "2024-01-01", "total_meters_climbed": 800, "total_distance": 12, "completion_time_hours": 4, "star_rating": 3})
        self.assertEqual(res.status_code, 302)

    def test_add_climb_logged_in(self):
        self.client.login(username="tester", password="pass12345")
        m = Munro.objects.create(name="Cairn Gorm", height=1245, location="Aviemore", region="Highlands", difficulty_rating=3, description="Ptarmigan")
        url = reverse("munro_app:add_climb")
        res = self.client.post(url, {"munro": m.id, "climb_date": "2024-01-01", "total_meters_climbed": 700, "total_distance": 9, "completion_time_hours": 3, "star_rating": 4})
        self.assertEqual(res.status_code, 302)
        self.assertEqual(ClimbRecord.objects.filter(user=self.user, munro=m).count(), 1)

    def test_user_profile_auto_create(self):
        self.client.login(username="tester", password="pass12345")
        url = reverse("munro_app:user_profile")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
