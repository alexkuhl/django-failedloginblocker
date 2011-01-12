"""Admin settings for the failedloginblocker module"""

from django.contrib import admin
from failedloginblocker.models import FailedAttempt

class AdminFailedAttempt( admin.ModelAdmin ):
    list_display = ( 'username', 'failures', 'timestamp', 'blocked' )
    search_fields = ( 'username', )

admin.site.register( FailedAttempt, AdminFailedAttempt )
