from functools import reduce

from django.conf import settings
from django.db import models


class Tier(models.Model):
    name = models.CharField(max_length=25)
    sequence = models.IntegerField(unique=True)
    no_of_compounds = models.IntegerField()
    bonus_start_perc = models.FloatField()
    bonus_multiplier = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sequence',)

    @classmethod
    def schedule(cls) -> []:
        current_bonus_mx = 0.0000
        schedule_ = []
        for tier in cls.objects.all():
            current_tier_mx = 0
            sequence_sig = 0.000
            for i in range(0, tier.no_of_compounds):
                # print(f"{tier.sequence+sequence_sig:.4f},{tier.name},{current_bonus_mx:.4f},{3+3*current_bonus_mx:.4f}")
                schedule_.append({
                    'id': tier.sequence+sequence_sig,
                    'name': tier.name,
                    'bonus_mx_perc': current_bonus_mx * 100,
                    'bonus_total_perc': (settings.BASE_BONUS_PERC + settings.BASE_BONUS_PERC * current_bonus_mx) * 100
                })
                sequence_sig += 0.001
                current_bonus_mx += tier.bonus_multiplier
        return schedule_

    @classmethod
    def calculate_locked_amount_over_time(cls,
                                          starting_amt: int = 0,
                                          compounds_per_day: int = 0,
                                          days_compounding: int = 0) -> float:
        return reduce(
            lambda amt, epoch: amt * (1 + epoch['bonus_total_perc'] / compounds_per_day / 100),
            cls.schedule()[:compounds_per_day*days_compounding],
            starting_amt
        )
