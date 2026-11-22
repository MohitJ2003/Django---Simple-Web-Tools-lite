from django.test import TestCase
from django.urls import reverse

from .models import DailyNote


class DailyNotePersistenceTests(TestCase):
    def test_create_note_is_saved_and_loaded_by_calendar(self):
        response = self.client.post(
            reverse("create_daily_note"),
            data='{"date":"2026-11-11","text":"Persist this note","color":"#e53935"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        note_id = response.json()["id"]
        self.assertTrue(DailyNote.objects.filter(pk=note_id).exists())

        calendar_response = self.client.get(reverse("daily_notes_monthly"))
        self.assertContains(calendar_response, "Persist this note")

        delete_response = self.client.post(
            reverse("delete_daily_note", args=[note_id])
        )

        self.assertEqual(delete_response.status_code, 204)
        self.assertFalse(DailyNote.objects.filter(pk=note_id).exists())

    def test_invalid_note_is_not_saved(self):
        response = self.client.post(
            reverse("create_daily_note"),
            data='{"date":"2026-11-11","text":" ","color":"#e53935"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(DailyNote.objects.count(), 0)

    def test_calendar_loads_notes_for_requested_year(self):
        DailyNote.objects.create(
            note_date="2027-01-03",
            note_text="Next year's note",
            color="#e53935",
        )
        DailyNote.objects.create(
            note_date="2026-01-03",
            note_text="Prior year's note",
            color="#fb8c00",
        )

        response = self.client.get(
            reverse("daily_notes_monthly"),
            {"year": "2027"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Next year's note")
        self.assertNotContains(response, "Prior year's note")
        self.assertContains(response, "let year = 2027")

    def test_notes_can_be_created_and_deleted_outside_2026(self):
        response = self.client.post(
            reverse("create_daily_note"),
            data='{"date":"2027-01-03","text":"Future note","color":"#e53935"}',
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        note_id = response.json()["id"]
        self.assertEqual(
            self.client.post(reverse("delete_daily_note", args=[note_id])).status_code,
            204,
        )
