from django.shortcuts import render, redirect, get_object_or_404
from .models import Requisition, Candidate
from .forms import RequisitionForm, CandidateForm

# Home Page
def home(request):
    return render(request, "base.html")

# Dashboard
def dashboard(request):
    requisitions = Requisition.objects.all()
    total_candidates = Candidate.objects.count()
    sources = Candidate.objects.values("source").distinct()
    return render(request, "dashboard.html", {
        "requisitions": requisitions,
        "total_candidates": total_candidates,
        "sources": sources
    })

# List all Requisitions
def requisition_list(request):
    requisitions = Requisition.objects.all()
    return render(request, "requisitions.html", {"requisitions": requisitions})

# View a Specific Requisition (Funnel Data for each Requisition)
from collections import Counter
import json
from django.http import JsonResponse
def get_funnel_data(request, requisition_no):
    STAGE_ORDER = ['Reached Out', 'Consideration', 'Interview', 'Offers', 'Hire']
    stage_index = {stage: i for i, stage in enumerate(STAGE_ORDER)}

    requisition = get_object_or_404(Requisition, requisition_no=requisition_no)
    candidates = Candidate.objects.filter(requisition=requisition)

    # Count how many candidates reached *at least* each stage
    stage_counts = [0] * len(STAGE_ORDER)

    for candidate in candidates:
        if candidate.status in stage_index:
            reached_index = stage_index[candidate.status]
            for i in range(reached_index + 1):  # Include all stages before and including current
                stage_counts[i] += 1

    funnel_data = [
        {"label": stage, "y": stage_counts[i]}
        for i, stage in enumerate(STAGE_ORDER)
    ]

    return JsonResponse({"funnel_data": funnel_data})

def view_requisition(request, requisition_no):
    requisition = Requisition.objects.filter(requisition_no=requisition_no).first()

    if request.method == "POST":
        print("POST DATA:", request.POST)
        candidate_id = request.POST.get("candidate_id")
        new_status = request.POST.get("status")

        if candidate_id and new_status:
            candidate = Candidate.objects.filter(id=candidate_id).first()
            if candidate:
                candidate.status = new_status
                candidate.save()

    candidates = Candidate.objects.filter(requisition__requisition_no=requisition_no)

    # Charts
    source_counts = dict(Counter(candidates.values_list('source', flat=True)))
    status_counts = dict(Counter(candidates.values_list('status', flat=True)))

    return render(request, "requisition_detail.html", {
        "requisition": requisition,
        "candidates": candidates,
        "source_counts": json.dumps(source_counts),
        "status_counts": json.dumps(status_counts),
    })

# Search Candidates
def search_candidates(request):
    query = request.GET.get("q", "").strip()

    if query.isdigit():
        requisition = Requisition.objects.filter(requisition_no=query).first()
        if requisition:
            return redirect('view_requisition', requisition_no=requisition.requisition_no)
    
    # If not found or not a number
    return render(request, "search.html", {
        "query": query,
        "not_found": True
    })


# Add Requisition
def add_requisition(request):
    if request.method == "POST":
        form = RequisitionForm(request.POST)
        if form.is_valid():
            # Save requisition instance without committing to DB
            requisition = form.save(commit=False)

            # Get recruiter names from custom text input field
            recruiter_names = form.cleaned_data.get("recruiter_names", "")
            requisition.save()  # Save requisition to generate ID for M2M

            # Process recruiter names
            names = [name.strip() for name in recruiter_names.split(",") if name.strip()]
            for name in names:
                recruiter, _ = Recruiter.objects.get_or_create(name=name)
                requisition.recruiters.add(recruiter)

            return redirect("requisitions")
    else:
        form = RequisitionForm()
    return render(request, "add_requisition.html", {"form": form})


# Add Candidate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate, Requisition
from django.urls import reverse
def add_candidates(request):
    requisitions = Requisition.objects.all()

    if request.method == "POST":
        input_type = request.POST.get("input_type")
        requisition_no = request.POST.get("requisition_no")

        try:
            requisition = Requisition.objects.get(requisition_no=requisition_no)
        except Requisition.DoesNotExist:
            return render(request, "add_candidates.html", {
                "requisitions": requisitions,
                "error": "Requisition not found!",
            })

        if input_type == "form":
            Candidate.objects.create(
                requisition=requisition,
                name=request.POST.get("name"),
                experience=request.POST.get("experience"),
                phone_no=request.POST.get("phone_no"),
                company=request.POST.get("company"),
                current_ctc=request.POST.get("current_ctc"),
                expected_ctc=request.POST.get("expected_ctc"),
                designation=request.POST.get("designation"),
                source=request.POST.get("source"),
                status=request.POST.get("status"),
                remarks=request.POST.get("remarks"),
            )
            return redirect(f"/requisition/{requisition.requisition_no}/")

        elif input_type == "bulk":
            raw_data = request.POST.get("pasted_data", "").strip()
            print("Raw data received:", raw_data, flush=True)

            if raw_data:
                lines = [line.strip() for line in raw_data.splitlines() if line.strip()]
                print("Total lines parsed:", len(lines), flush=True)

                if len(lines) < 12:
                    print("Not enough lines for even 1 candidate + headers", flush=True)
                    return redirect(reverse("add_candidates"))

                headers = lines[:6]
                expected_headers = ["Name", "Experience", "Company", "CTC", "Designation", "Remarks"]

                if headers != expected_headers:
                    print("Headers don't match expected format:", headers, flush=True)
                    return redirect(reverse("add_candidates"))

                data_lines = lines[6:]
                candidates = []
                i = 0
                while i + 5 < len(data_lines):
                    try:
                        candidate = Candidate(
                            requisition=requisition,
                            name=data_lines[i],
                            experience=data_lines[i + 1],
                            company=data_lines[i + 2],
                            current_ctc=data_lines[i + 3],
                            designation=data_lines[i + 4],
                            remarks=data_lines[i + 5],
                            phone_no="",
                            expected_ctc="",
                            source=""
                        )
                        candidates.append(candidate)
                        print(f" Added candidate: {candidate.name}", flush=True)
                    except Exception as e:
                        print(f" Error parsing candidate at index {i}: {e}", flush=True)
                    i += 6

                if candidates:
                    Candidate.objects.bulk_create(candidates)
                    print(f" {len(candidates)} candidates successfully added!", flush=True)
                else:
                    print(" No candidates to add", flush=True)

                return redirect(f"/requisition/{requisition.requisition_no}/")
            
    return render(request, "add_candidates.html", {"requisitions": requisitions})


                
def edit_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    requisitions = Requisition.objects.all()  # In case you want to allow changing requisition too

    if request.method == "POST":
        candidate.name = request.POST.get("name")
        candidate.experience = request.POST.get("experience")
        candidate.phone_no = request.POST.get("phone_no")
        candidate.company = request.POST.get("company")
        candidate.current_ctc = request.POST.get("current_ctc")
        candidate.expected_ctc = request.POST.get("expected_ctc")
        candidate.designation = request.POST.get("designation")
        candidate.source = request.POST.get("source")
        candidate.status = request.POST.get("status")
        candidate.remarks = request.POST.get("remarks")
        candidate.save()
        return redirect(f"/requisition/{candidate.requisition.requisition_no}/")

    return render(request, "edit_candidate.html", {
        "candidate": candidate,
        "requisitions": requisitions
    })

# General Funnel Data
def get_general_funnel_data(request):
    STAGE_ORDER = [
        "Reached Out",
        "Consideration",
        "Interview",
        "Offers",
        "Hire"
    ]
    stage_index = {stage: i for i, stage in enumerate(STAGE_ORDER)}

    candidates = Candidate.objects.all()

    # Initialize stage counts
    stage_counts = [0] * len(STAGE_ORDER)

    for candidate in candidates:
        if candidate.status in stage_index:
            reached_index = stage_index[candidate.status]
            for i in range(reached_index + 1):  # Add to all earlier stages
                stage_counts[i] += 1

    funnel_data = [
        {"label": stage, "y": stage_counts[i]}
        for i, stage in enumerate(STAGE_ORDER)
    ]

    return JsonResponse({"funnel_data": funnel_data})


# General Dashboard (Sources Pie Chart)
from collections import Counter
import json

def general_dashboard(request):
    candidates = Candidate.objects.all()
    print(f"Total Candidates: {candidates.count()}")  # Check how many

    for c in candidates:
        print(f"Candidate Source: {c.source}")  # See their source field

    source_counts = dict(Counter(c.source for c in candidates if c.source))
    print("SOURCE COUNTS:", source_counts)  # Final source check

    context = {
        'source_counts': json.dumps(source_counts),
        'total_candidates': candidates.count()
    }

    return render(request, 'dashboard.html', context)

def requisition_detail(request, requisition_no):
    requisition = get_object_or_404(Requisition, requisition_no=requisition_no)
    candidates = Candidate.objects.filter(requisition__requisition_no=requisition_no)

    return render(request, "requisition_detail.html", {
        "requisition": requisition,
        "candidates": candidates
    })

def delete_candidate(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    requisition_no = candidate.requisition.requisition_no 
    candidate.delete()
    return redirect('view_requisition', requisition_no=requisition_no)

# HR Metrics Page
from django.db.models import Sum, Q
from django.shortcuts import render
from .models import Requisition, Candidate

def hr_metrics_view(request):
    total_vacancies = Requisition.objects.aggregate(total=Sum('vacancies'))['total'] or 0

    candidates = Candidate.objects.all()
    total_candidates = candidates.count()

    # Cumulative logic
    total_reached_out = candidates.filter(
        Q(status="Reached Out") |
        Q(status="Consideration") |
        Q(status="Interview") |
        Q(status="Offers") |
        Q(status="Hire")
    ).count()

    total_considered = candidates.filter(
        Q(status="Consideration") |
        Q(status="Interview") |
        Q(status="Offers") |
        Q(status="Hire")
    ).count()

    total_interviewed = candidates.filter(
        Q(status="Interview") |
        Q(status="Offers") |
        Q(status="Hire")
    ).count()

    total_offers = candidates.filter(
        Q(status="Offers") |
        Q(status="Hire")
    ).count()

    total_hires = candidates.filter(status="Hire").count()

    context = {
        "total_vacancies": total_vacancies,
        "total_candidates": total_candidates,
        "total_reached_out": total_reached_out,
        "total_considered": total_considered,
        "total_interviewed": total_interviewed,
        "total_offers": total_offers,
        "total_hires": total_hires,
    }

    return render(request, "hr_metrics.html", context)

from django.http import JsonResponse
from django.db.models import Q
from .models import Requisition, Candidate

def get_hr_metrics_per_requisition(request):
    requisition_no = request.GET.get('requisition_no')

    try:
        req = Requisition.objects.get(requisition_no=requisition_no)
        candidates = Candidate.objects.filter(requisition=req)

        metrics = {
            "requisition": str(req),
            "vacancies": getattr(req, "vacancies", 0) or 0,
            "reached_out": candidates.count(),
            "considered": candidates.filter(Q(status__in=["Consideration", "Interview", "Offers", "Hire"])).count(),
            "interviewed": candidates.filter(Q(status__in=["Interview", "Offers", "Hire"])).count(),
            "offers": candidates.filter(Q(status__in=["Offers", "Hire"])).count(),
            "hires": candidates.filter(status="Hire").count()
        }

        return JsonResponse({"metrics": metrics})

    except Requisition.DoesNotExist:
        return JsonResponse({"error": "Requisition not found."}, status=404)

# Recruiter View
from .models import Recruiter
from django.db.models import Count

def recruiter_view(request):
    recruiters = Recruiter.objects.all()
    selected_recruiter = None
    requisitions = []

    # Recruiter performance (all recruiters and their requisition counts)
    performance_data = Recruiter.objects.annotate(
        requisition_count=Count('requisitions')
    ).values('name', 'requisition_count')

    if request.method == "POST":
        recruiter_id = request.POST.get("recruiter")
        if recruiter_id:
            selected_recruiter = Recruiter.objects.get(id=recruiter_id)
            requisitions = Requisition.objects.filter(recruiters=selected_recruiter)

            if "search_btn" in request.POST:
                search_query = request.POST.get("search_query", "").strip()
                if search_query:
                    requisitions = requisitions.filter(
                        Q(requisition_no__icontains=search_query) |
                        Q(job_title__icontains=search_query)
                    )

    return render(request, "recruiter_view.html", {
        "recruiters": recruiters,
        "selected_recruiter": selected_recruiter,
        "requisitions": requisitions,
        "performance_data": list(performance_data),
    })

# Edit Requiition button
from .forms import EditRequisitionForm

def edit_requisition_redirect(request):
    requisition_no = request.GET.get('requisition_no')
    if requisition_no:
        return redirect('edit_requisition', requisition_no=requisition_no)
    return render(request, 'requisitions.html')

def edit_requisition(request, requisition_no):
    requisition = get_object_or_404(Requisition, requisition_no=requisition_no)
    if request.method == 'POST':
        form = EditRequisitionForm(request.POST, instance=requisition)
        if form.is_valid():
            form.save()
            return redirect('view_requisition', requisition_no=requisition_no)
    else:
        form = EditRequisitionForm(instance=requisition)
    return render(request, 'edit_requisition.html', {'form': form, 'requisition_no': requisition_no})
