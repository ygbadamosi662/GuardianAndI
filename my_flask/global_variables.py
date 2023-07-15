#!/usr/bin/python3

"""
    Initializes bcrypt
"""

import bcrypt


globalBcrypt = bcrypt

# INSTANCES
GUARDIAN = 'guardians'
SCHOOL = 'schools'
STUDENT = 'students'
GUARD = 'guards'
REGISTRY = 'registries'
PICK_AND_DROP = 'pick_and_drops'
NOTIFICATION = 'notifications'
JWT_BLACKLIST = ''

# Notification auto-notes, if d the notification is not a chat notification +
# then you will probably need one of this
AUTHORIZATION = 'AUTHORIZATION_APP'
CONFIRMATION = 'CONFIRMATION_APP'
EMERGENCY = 'EMERGENCY'
CONFLICT = 'CONFLICT ALERT'
UNLINKED = 'UNLINKED'
