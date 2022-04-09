from sheetcake import Account, Array


array_a = Array(array=(1, 2, 3), name='a')
array_b = Array(array=(10, 20, 30), name='b')
acco = Account(array_a, array_b)

# print("Setup complete ===================================")
# print(acco.bbal[1])
acco.bbal.set_value(1, 200)
# print(acco.bbal[1])
assert acco.bbal[1].value == 200

print(f"acco.ebal[0].value: {acco.ebal[0].value}")
array_a[0].value = 100
# print(f"ebal: {acco.ebal[0].value}")
assert acco.ebal[0].value == 110

print("acco.ebal[0].value: ", acco.ebal[0].value)
print("acco.ebal[1].value: ", acco.ebal[1].value)
print("acco.ebal[2].value: ", acco.ebal[2].value)
