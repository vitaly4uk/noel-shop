#-*- coding:utf-8 -*-
"""
Custom comment model

Author:
    Vitaly Omelchuk <vitaly.omelchuk@gmail.com>
"""
from captcha.fields import CaptchaField
from django.contrib.comments.models import Comment

class CommentWithCaptcha(Comment):
    """
    Customize deffault comment models with captcha field
    """
    captcha = CaptchaField()

