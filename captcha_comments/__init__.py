# -*- coding:utf-8 -*-
"""
Custom comment application that add captcha field in every comment form

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""
from django.contrib.comments.models import Comment
from captcha_comments.forms import CommentFormWithCaptcha

def get_model():
    """ return custom comment model """
    return Comment

def get_form():
    """ return custom comment form """
    return CommentFormWithCaptcha

