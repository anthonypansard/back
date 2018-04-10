from django.core.management.base import BaseCommand
from BDD.models import Beamy, BeamyUser
from storage.models import FileImage, FileSong, FileVideo, FileUser
from alarm.models import Alarm
from django.contrib.auth.models import User
import os
from back.settings.base import BASE_DIR
from storage.models import EXT_IMAGE, EXT_VIDEO, EXT_SONG
from django.core.files import File

root = os.path.join(BASE_DIR, "../../testfiles/")

beamy = [
    {"name" : "bedroom"   , "version" : "1.0", "pin" : 1234},
    {"name" : "livingroom", "version" : "1.0", "pin" : 1111},
    {"name" : "restroom"  , "version" : "1.0", "pin" : 4321}]

user = [
    {"username" : "vader" , "password" : "azerty"},
    {"username" : "solo"  , "password" : "qwerty"}]

beamy_user = [
    {"beamy" : "bedroom"   , "user" : "vader", "right" : "owner"},
    {"beamy" : "livingroom", "user" : "solo" , "right" : "owner"},
    {"beamy" : "restroom"  , "user" : "solo" , "right" : "owner"},]

alarms = [
    {"beamy" : "bedroom", "day": "monday, tuesday, wednesday, thursday, friday", "hour" :  8, "minute": 0, "enabled" : "true" },
    {"beamy" : "bedroom", "day": "saturday"                                     , "hour" : 10, "minute": 0, "enabled" : "false"}]

def getFiles(ext):
    paths = []
    for _, _, files in os.walk(root):
        for file in files:
            if file.split('.')[-1].lower() in ext:
                paths.append(file)
    return paths

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_beamy(self):
        for b in beamy:
            try:
                Beamy.objects.get(name=b["name"])

            except:
                newb = Beamy(name=b["name"], id_version=b["version"], pin=b["pin"])
                newb.save()

    def _create_user(self):
        for u in user:
            try:
                User.objects.get(username=u["username"])

            except:
                newu = User(username=u["username"], password=u["password"])
                newu.save()

    def _create_beamy_user(self):
        for bu in beamy_user:
            try:
                BeamyUser.objects.get(
                    id_beamy__name=bu["beamy"], id_user__username=bu["user"])

            except:
                u = User.objects.get(username=bu["user"])
                b = Beamy.objects.get(name=bu["beamy"])
                newbu = BeamyUser(id_beamy=b, id_user=u, right=bu["right"])
                newbu.save()

    def _create_image(self):
        paths = getFiles(EXT_IMAGE)

        for path in paths:
            try:
                FileImage.objects.get(name = os.path.splitext(path)[0])

            except:
                file_path = os.path.join(root, path)
                image = FileImage(name = os.path.splitext(path)[0], image=File(open(file_path, 'rb')))
                image.save()

    def _create_video(self):
        paths = getFiles(EXT_VIDEO)

        for path in paths:
            try:
                FileVideo.objects.get(name = os.path.splitext(path)[0])

            except:
                file_path = os.path.join(root, path)
                video = FileVideo(name = os.path.splitext(path)[0], video=File(open(file_path, 'rb')))
                video.save()

    def _create_song(self):
        paths = getFiles(EXT_SONG)

        for path in paths:
            try:
                FileSong.objects.get(name = os.path.splitext(path)[0])

            except:
                file_path = os.path.join(root, path)
                song = FileSong(name = os.path.splitext(path)[0], song=File(open(file_path, 'rb')))
                song.save()
    
    def _create_alarm(self):
        for a in alarms:
            try:
                Alarm.objects.get(
                    beamy = a['beamy'],
                    day = a['day'],
                    hour = a['hour'])
            except:
                b = Beamy.objects.get(name = a['beamy'])
                alarm = Alarm(beamy = b, day = a['day'], hour = a['hour'], minute = a['minute'], enabled = a['enabled'])
                alarm.save()

    def handle(self, *args, **options):
        self._create_beamy()
        self._create_user()
        self._create_beamy_user()
        self._create_image()
        self._create_video()
        self._create_song()
        self._create_alarm()