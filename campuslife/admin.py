from django.contrib import admin
from .models import Picture, Interior, Rating, Review, Question, Answer, Reply, Room, Agent, Order, Wallet, AgentEarning


class PictureModelAdmin(admin.ModelAdmin):
    ordering = ['lodge_name']


admin.site.register(Picture, PictureModelAdmin)
admin.site.register(Interior)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Reply)
admin.site.register(Room)
admin.site.register(Agent)
admin.site.register(AgentEarning)
admin.site.register(Wallet)
admin.site.register(Order)
