import sys
from app import runserver

if 'run' in sys.argv:
    runserver()
elif '--set-email-password' in sys.argv:
    from app.helper_functions import set_email_password
    set_email_password()
