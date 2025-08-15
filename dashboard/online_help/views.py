from django.shortcuts import render

# Create your views here.
from collections import defaultdict, Counter
import json
import math
import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.db.models import Prefetch, F, Value, CharField
from django.db.models.functions import Coalesce

from .models import (
    Document, Section, Subsection, Writer, Task
)
# from .forms import (

# )

def home_test(request):
    ctx = {
        'title': 'Online Help Home',
        'message': 'Welcome to the Online Help Dashboard!'
    }
    return render(request, 'online_help/home_test.html', ctx)
