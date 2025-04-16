from django import forms
from .models import Requisition, Candidate

class RequisitionForm(forms.ModelForm):
    # Custom text field for recruiter names
    recruiter_names = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter recruiter names, comma-separated', 'size': '40'}),
        label='Recruiters'
    )

    class Meta:
        model = Requisition
        fields = ["requisition_no", "department", "vacancies", "job_title"]

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ["requisition", "name", "experience", "phone_no", "company", "current_ctc", "expected_ctc", "designation", "source", "status", "remarks"]

class EditRequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['job_title', 'recruiters', 'vacancies']
        widgets = {
            'recruiters': forms.CheckboxSelectMultiple(),
        }
