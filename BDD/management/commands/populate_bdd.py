from django.core.management.base import BaseCommand
from BDD.models import Beamy, BeamyUser
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_beamy(self):
        try :
            Beamy.objects.get(name = 'death_star')

        except:
            bdeath_star = Beamy(name = 'death_star', id_version = '1.0', pin = 1234)
            bdeath_star.save()

        try:            
            Beamy.objects.get(name = 'falcon')

        except:
            bfalcon = Beamy(name = 'falcon', id_version = '1.0', pin = 4321)
            bfalcon.save()
    
    def _create_user(self):
        try :
            User.objects.get(username = 'vador')

        except:
            uvador = User(username = 'vador', password = "azerty")
            uvador.save()
        
        try :
            User.objects.get(username = 'solo')

        except:
            usolo = User(username = 'solo', password = "azerty")
            usolo.save()
    
    def _create_beamy_user(self):
        try :
            BeamyUser.objects.get(id_beamy__name = 'death_star', id_user__username = 'vador')
            
        except:
            vador = User.objects.get(username = 'vador')
            death_star = Beamy.objects.get(name = 'death_star')
            budv = BeamyUser(id_beamy = death_star, id_user = vador, right = 'owner')
            budv.save()
        
        try :
            BeamyUser.objects.get(id_beamy__name = 'falcon', id_user__username = 'solo')

        except:
            solo = User.objects.get(username = 'solo')
            falcon = Beamy.objects.get(name = 'falcon')
            bufs = BeamyUser(id_beamy = falcon, id_user = solo, right = 'owner')
            bufs.save()
    
    def handle(self, *args, **options):
        self._create_beamy()
        self._create_user()
        self._create_beamy_user()