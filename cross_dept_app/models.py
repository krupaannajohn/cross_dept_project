from django.db import models

class Recruiter(models.Model):
    name = models.CharField(max_length=100)
    #emp_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name}"
    
class Requisition(models.Model):
    requisition_no = models.CharField(max_length=20, unique=True)
    DEPARTMENT_CHOICES = [
        ("Administration", "Administration"),
        ("Appliance Division", "Appliance Division"),
        ("Brand & Communications", "Brand & Communications"),
        ("Category Strategy & NBI", "Category Strategy & NBI"),
        ("Civil & MEP", "Civil & MEP"),
        ("Corporate Manufacturing Services", "Corporate Manufacturing Services"),
        ("Customer Service", "Customer Service"),
        ("ECDI Service", "ECDI Service"),
        ("Electromechanical Division", "Electromechanical Division"),
        ("Electronics Division", "Electronics Division"),
        ("Emerging Channels & Digital Initiatives", "Emerging Channels & Digital Initiatives"),
        ("Finance & Accounts", "Finance & Accounts"),
        ("Go To Market", "Go To Market"),
        ("Human Resources", "Human Resources"),
        ("Industrial Design", "Industrial Design"),
        ("IT & Systems", "IT & Systems"),
        ("Legal", "Legal"),
        ("Marketing", "Marketing"),
        ("Mechanical & Electrical Division", "Mechanical & Electrical Division"),
        ("New Product Development", "New Product Development"),
        ("Quality", "Quality"),
        ("R&D (Electronics Division)", "R&D (Electronics Division)"), 
        ("Strategy", "Strategy"),
        ("Supply Chain Management", "Supply Chain Management"),
        ("Wires & Cables Division", "Wires & Cables Division")
    ]
    department = models.CharField(max_length=500, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    vacancies = models.IntegerField()
    job_title = models.CharField(max_length=100) 
    recruiters = models.ManyToManyField(Recruiter, related_name='requisitions')
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.requisition_no

class Candidate(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name="candidates")
    name = models.CharField(max_length=100, blank=True, null=True)
    experience = models.FloatField(blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    current_ctc = models.CharField(max_length=100, blank=True, null=True)
    expected_ctc = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    SOURCE_CHOICES = [
        ('Naukri', 'Naukri'),
        ('Linkedin', 'Linkedin'),
        ('Indeed', 'Indeed'),
        ('Employee Referral', 'Employee Referral')
    ]
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES, blank=True, null=True)
    STATUS_CHOICES = [
        ('Reached Out', 'Reached Out'),
        ('Consideration', 'Consideration'),
        ('Interview', 'Interview'),
        ('Offers', 'Offers'),
        ('Hire','Hire')
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
