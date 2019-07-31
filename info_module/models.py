from django.db import models

# Create your models here.
class directorate(models.Model):
    directorate_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,blank=True)
    address=models.TextField(max_length=1000,blank=True)
    phone=models.CharField(max_length=20,blank=True)
    email=models.CharField(max_length=70,blank=True)
    fax=models.CharField(max_length=70,blank=True)
    title=models.CharField(max_length=250,blank=True)
    description=models.TextField(max_length=1000,blank=True)
    caption=models.CharField(max_length=500,blank=True)
    logo=models.CharField(max_length=250,blank=True)


class studycentre(models.Model):
    studycentre_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,blank=True)
    address=models.TextField(max_length=1000,blank=True)
    phone=models.CharField(max_length=20,blank=True)
    location=models.CharField(max_length=250,blank=True)
    managed_by=models.CharField(max_length=250,blank=True)

class Department(models.Model):
    Department_id = models.AutoField(primary_key=True)
    Department_Name = models.CharField(max_length=100,blank=True)
    Department_description=models.TextField(max_length=3000,blank=True)
    meta_tag=models.CharField(max_length=150,blank=True)
    Department_code=models.CharField(max_length=45,blank=True)

class Course(models.Model):
    course_id=models.AutoField(primary_key=True)
    course_code=models.CharField(max_length=100,blank=True)
    course_name=models.CharField(max_length=100,blank=True)
    credit=models.CharField(max_length=100,blank=True)
    internal_mark=models.IntegerField()
    external_mark=models.IntegerField()
    total_mark=models.IntegerField()

class events(models.Model):
    event_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=500,blank=True)
    description=models.TextField(max_length=1000,blank=True)
    start_date=models.DateField()
    end_date=models.DateField()
    picture=models.CharField(max_length=250,blank=True)


class gallerytitle(models.Model):
    title_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=500,blank=True)


class images(models.Model):
    image_id=models.AutoField(primary_key=True)
    photo=models.CharField(max_length=500,blank=True)
    date=models.DateField()
    thumbnail=models.CharField(max_length=250,blank=True)
    title_id=models.ForeignKey(gallerytitle, on_delete=models.CASCADE)


class achievements(models.Model):
    achievement_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=500,blank=True)
    description=models.TextField(max_length=2000,blank=True)
    picture=models.CharField(max_length=500,blank=True)

class aboutus(models.Model):
    aboutus_id=models.AutoField(primary_key=True)
    description=models.TextField(max_length=20000,blank=True)

class Faq(models.Model):
    faq_id = models.AutoField(primary_key=True)
    question = models.TextField(max_length=500)
    answer = models.TextField(max_length=500)


class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    docFile = models.CharField(max_length=100)

class Announcement(models.Model):
    announcements_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

class ResearchPublication(models.Model):
    research_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    guide = models.CharField(max_length=100)
    synopsis = models.TextField(max_length=1000)
    research_documents = models.CharField(max_length=500)

class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=2000)
    image = models.CharField(max_length=100)

class ActsAndRegulation(models.Model):
    act_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    document = models.CharField(max_length=100)

class Slider(models.Model):
    slider_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=2000)
    image = models.CharField(max_length=100)

class Programme(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_code = models.CharField(max_length=100,blank=True)
    title=models.CharField(max_length=300,blank=True)
    description = models.TextField(max_length=20000,blank=True)
    department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    programme_Struture = models.CharField(max_length=1000,blank=True)
    syllabus = models.CharField(max_length=1000,blank=True)
    brochure = models.CharField(max_length=1000,blank=True)
    status=models.CharField(max_length=300,blank=True)
    thumbnail = models.CharField(max_length=100,blank=True)
    meta_tag=models.CharField(max_length=300,blank=True)
    eligibility =models.TextField(max_length=20000,blank=True)
    program_type=models.CharField(max_length=10,blank=True)
    no_of_semester=models.IntegerField()

class Course_programme_mapping(models.Model):
    course_prg_id=models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE)
    prg_id=models.ForeignKey(Programme,on_delete=models.CASCADE)
    
class Notify(models.Model):
    notify_id = models.AutoField(primary_key=True)
    notify_title=models.CharField(max_length=1000)
    notify_status=models.CharField(max_length=100)

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    program_id = models.ForeignKey(Programme, on_delete=models.CASCADE)
    department_id=models.ForeignKey(Department, on_delete=models.CASCADE)
    study_centre_id = models.ForeignKey(studycentre,on_delete=models.CASCADE)
    batch_name=models.CharField(max_length=500)
    no_of_seats=models.IntegerField()
    appli_start_date=models.DateField()
    appli_end_date=models.DateField()
    prgm_start_date=models.DateField()
    prgm_end_date=models.DateField()
    status=models.CharField(max_length=100)
    program_fee=models.CharField(max_length=100)
    batch_dis_name=models.CharField(max_length=500)

class Highlights(models.Model):
    highlights_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=20000,blank=True)

class ProgramEligibility(models.Model):
    eligibility_id=models.AutoField(primary_key=True)
    program_id=models.ForeignKey(Programme, on_delete=models.CASCADE)
    eligibility_question=models.CharField(max_length=2000,blank=True)
    default_answer=models.BooleanField(default=False)
    is_mandatory=models.BooleanField(default=False)

class StudentApplicants(models.Model):
    student_id=models.AutoField(primary_key=True)
    batch_id=models.ForeignKey(Batch, on_delete=models.CASCADE)
    user_id=models.CharField(max_length=100)
    program_id=models.ForeignKey(Programme, on_delete=models.CASCADE)
    applied_date=models.DateTimeField()
    applicant_status=models.CharField(max_length=100)	
    course_fee =models.CharField(max_length=100)
    transaction_id=models.CharField(max_length=500)
    applicant_id=models.CharField(max_length=100)
    is_paid=models.BooleanField(default=False)

class PaymentHistory(models.Model):
    pay_id=models.AutoField(primary_key=True)
    user_id=models.CharField(max_length=100)
    prgm_id = models.CharField(max_length=100)
    applicant_no=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100)
    trans_id=models.CharField(max_length=500)
    trans_amount=models.CharField(max_length=100)
    trans_date=models.DateTimeField()
    res_code=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    res_msg=models.CharField(max_length=100)
    total_fee=models.CharField(max_length=100)
    trans_res=models.CharField(max_length=1000)

