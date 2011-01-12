"""
Makes use of the FLB_MAX_FAILURES and FLB_BLOCK_INTERVAL values in
settings.py. If these are not present, default values of 5 failures
and 1 day are used.

The easiest way to remove a block is to delete the FailedAttempt record (e.g.
via the admin).
"""

from django.db import models
from datetime import datetime, timedelta
from django.conf import settings

# default values that can be overriden in settings.py
FLB_MAX_FAILURES = int( getattr( settings, 'FLB_MAX_FAILURES', 5 ) )
FLB_BLOCK_INTERVAL = int( getattr( settings, 'FLB_BLOCK_INTERVAL', 1440 ) )

class FailedAttempt( models.Model ):
    username = models.CharField( 'Username', max_length=255 )
    failures = models.PositiveIntegerField( 'Failures', default=0 )
    timestamp = models.DateTimeField( 'Last failed attempt', auto_now=True )

    def too_many_failures( self ):
        """ 
        Check if the minimum number of failures needed for a block
        has been reached 
        """
        return self.failures >= FLB_MAX_FAILURES

    def recent_failure( self ):
        """
        Checks if the timestamp one the FailedAttempt object is
        recent enough to result in an increase in failures
        """
        return datetime.now( ) < self.timestamp + timedelta( \
               minutes=FLB_BLOCK_INTERVAL )

    def blocked( self ):
        """ 
        Shortcut function for checking both too_many_failures 
        and recent_failure 
        """
        return self.too_many_failures( ) and self.recent_failure( )
    blocked.boolean = True

    def __unicode__(self):
        return u'%s (%d failures until %s): ' % \
               ( self.username,self.failures, self.timestamp )

    class Meta:
        ordering = [ '-timestamp' ]