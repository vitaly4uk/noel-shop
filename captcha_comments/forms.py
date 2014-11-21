# -*- coding:utf-8 -*-
"""
Custom comment form

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""
from captcha.fields import CaptchaField
from django.contrib.comments.forms import CommentForm
from django.contrib.comments.models import Comment

class CommentFormWithCaptcha(CommentForm):
    captcha = CaptchaField()

    #def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
    #    return Comment

    #def get_comment_create_data(self):
        # Use the data of the superclass, and add in the title field
    #    data = super(CommentFormWithCaptcha, self).get_comment_create_data()
    #    data['title'] = self.cleaned_data['title']
    #    return data

