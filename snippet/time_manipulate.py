import arrow

arrow.now()
arrow.utcnow()

presents = arrow.now()
a_year_before = presents.replace(years=-1)


start = arrow.now().replace(years=-1)
end = arrow.now()
for r in arrow.Arrow.range('day', start, end):
    print(r.format('YYYY-MM-DD'))
