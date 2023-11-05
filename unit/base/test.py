from base_binding import BaseBinding

unit1 = BaseBinding()
unit2 = BaseBinding()

unit1.bindings['2'] = []
unit1.bind('2', unit2)
print(unit1.bindings)