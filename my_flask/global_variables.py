#!/usr/bin/python3

"""
    Initializes bcrypt
"""

import bcrypt


globalBcrypt = bcrypt

# INSTANCES
GUARDIAN = 'GUARDIAN'
SCHOOL = 'SCHOOL'
STUDENT = 'STUDENT'
GUARD = 'GUARD'
REGISTRY = 'REGISTRY'
PICK_AND_DROP = 'PICK_AND_DROP'
NOTIFICATION = 'NOTIFICATION'

# Notification auto-notes, if d the notification is not a chat notification +
# then you will probably need one of this
AUTHORIZATION = 'AUTHORIZATION_APP'
CONFIRMATION = 'CONFIRMATION_APP'
EMERGENCY = 'EMERGENCY'
CONFLICT = 'CONFLICT ALERT'
