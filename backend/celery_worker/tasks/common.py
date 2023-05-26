# -*- coding: utf-8 -*-
# @author: xiaobai

from celery_worker.worker import celery


@celery.task
def add(i):
    return 1 + i
