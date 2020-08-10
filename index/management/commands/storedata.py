import json
import os
from django.core.management.base import BaseCommand
from index.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_objs = News.objects.all()
        if all_objs:
            all_objs.delete()
        cwd = os.getcwd()
        path = cwd+"\\data"
        filename_set = os.listdir(path)
        i = 0
        for filename in filename_set:
            with open(path+"\\"+filename, encoding='utf-8') as file:
                data = json.load(file)
                News.objects.create(id=i, title=data['title'], source=data['source'], time=data['time'], content=data['content'])
                i += 1
