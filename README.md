# UniverseMoneyCalculator

This is a quick-and-dirty calculator for the crypto currency project [univ.money](https://univ.money/), based on Universe's tier system.

The calculator gives you the ability to put it in your current value and provide different lengths of time of compounding and waiting before collecting. Example, one node (42,000 UNIV), compounded 5 times a day for 5 days and waiting another 5 days will yield 8212 UNIV.

To run:
  1. clone
  2. create a virtualenv and `pip install -r requirements.txt`
  3. make sure settings.BASE_BONUS_PERC is still accurate.
  4. run `python manage.py migrate`
  5. run `python manage.py createsuperuser` (if you want to access the admin)
  6. run `python manage.py loaddata 001_tiers` 
  7. run `python manage.py runserver`
  8. Go to http://localhost:8000/

TODOs: 
* Add option for scenarios like "When will I break even" or "What happens if I collect every x days"
* Add charting

