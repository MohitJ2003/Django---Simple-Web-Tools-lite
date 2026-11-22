import json
import os
import re
from datetime import date

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from openpyxl.reader.excel import load_workbook
from django.views.decorators.http import require_POST

from .models import DailyNote
from .forms import MyForm, CreateNewBillFile
base_path = os.path.dirname(os.path.abspath(__file__))
# print("Base Path - " + base_path)

def daily_notes_Monthly(request):
    year_value = request.GET.get("year", "2026")
    try:
        calendar_year = int(year_value)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("A valid calendar year is required.")

    if not 1 <= calendar_year <= 9999:
        return HttpResponseBadRequest("Calendar year must be between 1 and 9999.")

    notes = [
        {
            "id": note.pk,
            "date": note.note_date.isoformat(),
            "text": note.note_text,
            "color": note.color,
        }
        for note in DailyNote.objects.filter(note_date__year=calendar_year)
    ]
    return render(
        request,
        'MonthlyClanderNov2026.html',
        {"notes": notes, "calendar_year": calendar_year},
    )


@require_POST
def create_daily_note(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    note_date_value = payload.get("date")
    note_text = payload.get("text")
    color = payload.get("color")
    if not isinstance(note_date_value, str):
        return JsonResponse({"error": "A valid note date is required."}, status=400)

    try:
        note_date = date.fromisoformat(note_date_value)
    except ValueError:
        return JsonResponse({"error": "A valid note date is required."}, status=400)

    if not isinstance(note_text, str) or not note_text.strip():
        return JsonResponse({"error": "Note text cannot be empty."}, status=400)
    if not isinstance(color, str):
        return JsonResponse({"error": "A valid note color is required."}, status=400)

    note = DailyNote(
        note_date=note_date,
        note_text=note_text.strip(),
        color=color,
    )
    try:
        note.full_clean()
    except ValidationError as error:
        return JsonResponse({"error": "; ".join(error.messages)}, status=400)

    note.save()
    return JsonResponse(
        {
            "id": note.pk,
            "date": note.note_date.isoformat(),
            "text": note.note_text,
            "color": note.color,
        },
        status=201,
    )


@require_POST
def delete_daily_note(request, note_id):
    note = get_object_or_404(DailyNote, pk=note_id)
    note.delete()
    return HttpResponse(status=204)
