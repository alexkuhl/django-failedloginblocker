class LoginBlockedError( Exception ):
  def __init__( self ):
    msg = "Your account has been locked due to too many failed login attempts."
    msg += " Contact us to have your account reactivated."
    super( LoginBlockedError, self ).__init__( msg )