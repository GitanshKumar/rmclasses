from django.db import models

# Create your models here.
class Registration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.BigIntegerField()
    course = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    registered_at = models.DateTimeField(auto_now_add=True)
    query = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.course}"
    
class Standard(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    level = models.SmallIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    courseID = models.SmallIntegerField()
    standards = models.ManyToManyField(Standard, related_name="courses")

    def class_range(self):
        """
        Returns a string representing the continuous range of class levels, e.g., "6-12".
        """
        # Extract numeric levels and sort
        levels = sorted(list(map(int, self.standards.values_list('name', flat=True))))

        if not levels:
            return ''

        # Initialize range tracking
        ranges = []
        start = prev = levels[0]

        for lvl in levels[1:]:
            if lvl == prev + 1:
                prev = lvl
            else:
                # close current range
                if start == prev:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{prev}")
                start = prev = lvl
        # append final range
        if start == prev:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{prev}")

        # Join multiple ranges with comma
        return ','.join(ranges)

    def __str__(self):
        return f"{self.name} {self.courseID}"

class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField()
    picture = models.ImageField(null=True, blank=True, default="profile/default user.png", upload_to="profile/")
    
    def __str__(self):
        return self.name