""" Decorators used by failedloginblocker """

from failedloginblocker.models import FailedAttempt
from failedloginblocker.exceptions import LoginBlockedError

def monitor_login( auth_func ):
    """
    Function that replaces Django authentication() function with one that 
    tracks failed logins and blocks further attempts based on a threshold
    """

    if hasattr( auth_func, '__PROTECT_FAILED_LOGINS__' ) :
        # avoiding multiple decorations
        return auth_func
    
    def decorate( *args, **kwargs ):
        """ Wrapper for Django authentication function """
        user = kwargs.get( 'username', '' )
        if not user:
            raise ValueError( 'username must be supplied by the \
                authentication function for FailedLoginBlocker to operate' )
                
        try:
            fa = FailedAttempt.objects.get( username=user )
            if fa.recent_failure( ):
                if fa.too_many_failures( ):
                    # block the authentication attempt because
                    # of too many recent failures
                    fa.failures += 1
                    fa.save( )
                    raise LoginBlockedError( )
            else:
                # the block interval is over, reset the count
                fa.failures = 0
                fa.save( )
        except FailedAttempt.DoesNotExist:
            fa = None

        result = auth_func( *args, **kwargs )
        if result:
            # the authentication was successful
            return result
        # authentication failed 
        fa = fa or FailedAttempt( username=user, failures=0 )
        fa.failures += 1
        fa.save( )
        # return with unsuccessful auth
        return None

    decorate.__PROTECT_FAILED_LOGINS__ = True
    return decorate
