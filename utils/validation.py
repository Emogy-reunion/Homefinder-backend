from email_validator import validate_email, EmailNotValidError
import re

def validate_firstname(firstname):
    '''
    checks to ensure that the first name is in the required format
    '''
    errors = []
    if not firstname:
        errors.append('First name is required!')
    elif len(firstname) < 2:
        errors.append('First name must be at least 2 characters long!')
    elif len(firstname) > 30:
        errors.append('First name must not exceed  30 characters long!')
    return errors


def validate_lastname(lastname):
    '''
    checks to ensure that the last name is in the required format
    '''
    errors = []
    if not lastname:
        errors.append('Last name is required!')
    elif len(lastname) < 2:
        errors.append('Last name must be at least 2 characters long!')
    elif len(lastname) > 30:
        errors.append('Last name must not exceed 30 characters long!')
    return errors

def check_email(email):
    '''
    makes the sure the email format is correct
    ensures that the  domain exists
    '''
    errors = []
    if not email:
        errors.append('Email is required!')
    elif len(email) > 5:
        errors.append('Email must be at least 5 characters long!')
    elif len(email) > 30:
        errors.append('Email must not exceed 30 characters long!')
    else:
        try:
            valid = validate_email(email, check_delivaribility=True)
        except EmailNotValidError as e:
            errors.append('Invalid email format!')
    return errors
