from django.core.management.base import BaseCommand
from storage.models import FileSong
import os
from back.settings.base import BASE_DIR
from storage.models import EXT_SONG
from django.core.files import File


root = os.path.join(BASE_DIR, "../media/ringtone/")


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _add_default_alarm(self):
        try:
            # Yep, this is harcoded
            FileSong.objects.get(name = os.path.splitext("default_ringtone_1111111111")[0])

        except:
            file_path = os.path.join(root, "default_ringtone_1111111111.mp3")
            song = FileSong(name = os.path.splitext("default_ringtone_1111111111")[0], song=File(open(file_path, 'rb')))
            song.save()


    def handle(self, *args, **options):
        self._add_default_alarm()