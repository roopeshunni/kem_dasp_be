from django.contrib import admin
from django.db import models
from .models import *

class directorateAdmin(admin.ModelAdmin):
    list_display=['directorate_id','name','address','phone','email','fax','title','description','caption','logo']
admin.site.register(directorate,directorateAdmin)


class studycentreAdmin(admin.ModelAdmin):
    list_display=['studycentre_id','name','address','phone','location','managed_by']
admin.site.register(studycentre,studycentreAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display=['course_id','course_code','course_name','credit','internal_mark','external_mark','total_mark']
admin.site.register(Course,CourseAdmin)

class eventsAdmin(admin.ModelAdmin):
    list_display=['event_id','title','description','start_date','end_date','picture']
admin.site.register(events,eventsAdmin)


class gallerytitleAdmin(admin.ModelAdmin):
    list_display=['title_id','title']
admin.site.register(gallerytitle,gallerytitleAdmin)


class imagesAdmin(admin.ModelAdmin):
    list_display=['image_id','photo','date','thumbnail','title_id']
admin.site.register(images,imagesAdmin)


class achievementsAdmin(admin.ModelAdmin):
    list_display=['achievement_id','title','description','picture']
admin.site.register(achievements,achievementsAdmin)


class aboutusAdmin(admin.ModelAdmin):
    list_display=['aboutus_id','description']
admin.site.register(aboutus,aboutusAdmin)


class FaqAdmin(admin.ModelAdmin):
	list_display = ['faq_id','question','answer']
admin.site.register(Faq,FaqAdmin)


class DocumentsAdmin(admin.ModelAdmin):
	list_display = ['document_id','title','docFile']
admin.site.register(Document,DocumentsAdmin)


class AnnouncementsAdmin(admin.ModelAdmin):
	list_display = ['announcements_id','title','description']
admin.site.register(Announcement,AnnouncementsAdmin)


class ResearchAdmin(admin.ModelAdmin):
	list_display = ['research_id','title','author','guide','synopsis','research_documents']
admin.site.register(ResearchPublication,ResearchAdmin)


class NewsAdmin(admin.ModelAdmin):
	list_display = ['news_id','title','description','image']
admin.site.register(News,NewsAdmin)


class ActsAdmin(admin.ModelAdmin):
	list_display = ['act_id','title','description','document']
admin.site.register(ActsAndRegulation,ActsAdmin)


class SliderAdmin(admin.ModelAdmin):
	list_display = ['slider_id','title','description','image']
admin.site.register(Slider,SliderAdmin)


class ProgramTableAdmin(admin.ModelAdmin):
	list_display=['program_id','program_code','title','description','department_id','programme_Struture','status','thumbnail','meta_tag','eligibility','syllabus','brochure']
admin.site.register(Programme,ProgramTableAdmin)

class ProgramCouseMapping(admin.ModelAdmin):
	list_display=['course_prg_id','course_id','prg_id']
admin.site.register(Course_programme_mapping,ProgramCouseMapping)


class NotifyAdmin(admin.ModelAdmin):
	list_display = ['notify_id','notify_title','notify_status']
admin.site.register(Notify,NotifyAdmin)

class BatchAdmin(admin.ModelAdmin):
	list_display = ['batch_id','program_id','department_id','batch_name','no_of_seats','appli_start_date','appli_end_date','prgm_start_date','prgm_end_date','status','program_fee']
admin.site.register(Batch,BatchAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display=['Department_id','Department_Name','Department_description']
admin.site.register(Department,DepartmentAdmin)

class HighlightsAdmin(admin.ModelAdmin):
	list_display=['highlights_id','description']
admin.site.register(Highlights,HighlightsAdmin)

class PaymentHistoryAdmin(admin.ModelAdmin):
	list_display=['pay_id','user_id']
admin.site.register(PaymentHistory,PaymentHistoryAdmin)
