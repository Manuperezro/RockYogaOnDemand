from django.db import models
from django.urls import reverse
from  embed_video.fields import EmbedVideoField
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

        # Meta clase to update the string values for the verbose name and it's plural
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('category-list', args=[self.slug])
    
    def __str__(self):
        return self.title

class Course(models.Model):
        """ Create Courses which will include list of videos """
        category = models.ForeignKey(Category, related_name='courses', null=True, on_delete=models.SET_NULL)
        price = models.FloatField(null=True)
        name = models.CharField(max_length=100)
        slug = models.SlugField(max_length=100, blank=True, unique=True)
        thumbnail = models.ImageField(upload_to='media/images/', null=True)
        sub_title = models.CharField(max_length=200)
        description = models.TextField(blank=True, null=True)
        active = models.BooleanField(null=True)
        created = models.DateField(auto_now_add=True)
        is_published = models.BooleanField(default=True)
        is_feautured = models.BooleanField(default=False)
         # user = models.ForeignKey(Student, on_delete=models.CASCADE)
        
        # The str here represent a course object each time is called, here will return course name.
        def __str__(self):
            return self.name


        def get_absolute_url(self):
            return reverse('course-detail', kwargs={
                'slug': self.slug
            })
        
        def get_formated_price(self):
            return "£{0:.2f}".format(self.price / 100) 
        
        # property to return all the sections of the course, and sorted byt the section's position property.
        @property
        def sections(self):
            return self.section_set.all().order_by('position')

class Section(models.Model):
    """In each section it will be a list of videos that belongs to this section """
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    position = models.IntegerField()

    def __str__(self):
        return self.title
    
    # property to return a list of the sections of videos and sort it by the section's Video's property.
    @property
    def videos(self):
        return self.video_set.all().order_by('position')


class Video(models.Model):
    """ This model will return a video object, the foreign key of this model will point to the videos model """
    section = models.ForeignKey(Section, related_name='videos', on_delete=models.CASCADE)
    video_url = EmbedVideoField()
    thumbnail = models.ImageField(upload_to='media/images', null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    position = models.IntegerField()
    
    # Return the section title
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video-detail', kwargs={
            "course_slug": self.section.course.slug,
            "slug": self.slug
        })

# pre_save method to autmatically generate the slug fields by adding dashes between words in the title with pre_save and slugify
# The instance here will be the catgory object



# def pre_save_category(sender, instance, *args, **kwargs):
#     # check if the category slug doen't exists and then vonvert the category title to the slug.
#     if not instance.slug:
#         instance.slug = slugify(instance.title)


def pre_save_course(sender, instance, *args, **kwargs):
     # check if the course slug doen't exists and then vonvert the category title to the slug.
    if not instance.slug:
        instance.slug = slugify(instance.name)


def pre_save_section(sender, instance, *args, **kwargs):
     # check if the section slug doen't exists and then vonvert the category title to the slug.
    if not instance.slug:
        instance.slug = slugify(instance.title)


def pre_save_video(sender, instance, *args, **kwargs):
     # check if the video slug doen't exists and then vonvert the category title to the slug.
    if not instance.slug:
        instance.slug = slugify(instance.title)


# pre_save.connect(pre_save_category, sender=Category)
pre_save.connect(pre_save_course, sender=Course)
pre_save.connect(pre_save_section, sender=Section)
pre_save.connect(pre_save_video, sender=Video)
    
