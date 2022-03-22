def pat():
  for i in range(0,4):
    for j in range(0,i+1):
      print(j+1,end="")
    print()
  for i in range(10):
    print(i+1,end="")
  print()
  for i in range(5,0,-1):
    for j in range(1,i):
      if (i == 3):
          print("1 2")
          break
      else:
          print(j,end="")
    print()
pat()
