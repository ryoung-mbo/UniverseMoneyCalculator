from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from calculator.models import Tier


def calculator(request):
    template = loader.get_template('calculator/index.html')
    # defaults
    context = {
        'starting_amt': 42000,
        'compounds_per_day': 0,
        'days_compounding': 0,
        'days_passive': 0,
        'current_epoch': Tier.schedule()[0],
        'total_locked': 42000,
        'daily_rewards': 0,
        'grand_total': 0,
    }
    if request.method == "GET":
        return HttpResponse(template.render(context, request))
    starting_amt = int(request.POST['starting_amt'])
    compounds_per_day = int(request.POST['compounds_per_day'])
    days_compounding = int(request.POST['days_compounding'])
    days_passive = int(request.POST['days_passive'])
    # no_of_compounds follows the schedule multiplying your total locked amount after every compound and increasing the
    # locked amount accordingly.
    total_locked = Tier.calculate_locked_amount_over_time(
        starting_amt=starting_amt,
        compounds_per_day=compounds_per_day,
        days_compounding=days_compounding
    )
    current_epoch = Tier.schedule()[compounds_per_day * days_compounding]
    bonus_total_perc = current_epoch['bonus_total_perc']
    daily_rewards = total_locked * bonus_total_perc / 100
    grand_total = daily_rewards * days_passive
    context = {
        'starting_amt': starting_amt,
        'compounds_per_day': compounds_per_day,
        'days_compounding': days_compounding,
        'days_passive': days_passive,
        'current_epoch': current_epoch,
        'total_locked': total_locked,
        'daily_rewards': daily_rewards,
        'grand_total': grand_total,
    }
    return HttpResponse(template.render(context, request))


def tier_schedule(request):
    schedule = Tier.schedule
    template = loader.get_template('calculator/schedule.html')
    context = {'data': schedule}
    return HttpResponse(template.render(context, request))
