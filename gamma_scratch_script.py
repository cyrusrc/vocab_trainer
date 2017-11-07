import matplotlib.pyplot as plt
import numpy.random as rand

values = []

i = 0
# currently the number of words in words.txt
ceil = 44506
"""
adjust level to see how probability density of index drawn varies with vocab level
"""
level = 25
# gamma distribution scale parameter
g_scale = ceil * 0.05
# exponential distribution scale parameter
e_scale = ceil * 0.1

while i < 10000:
    val = int(rand.gamma(level, g_scale))

    # COMMENT OUT TO SEE UNDAMPENED VALUES
    if val >= ceil:
        val = int(ceil - rand.exponential(e_scale))

    # UNCOMMENT TO SEE VALUES FOR EXPONENTIAL DISTRIBUTION (WHICH ARE USED AS DAMPENERS)
    # val = int(rand.exponential(e_scale))

    values.append(val)
    i += 1

values = sorted(values)

plt.hist(values, bins=100)
plt.xlabel("index of values drawn")
plt.ylabel("count of values")
plt.show()
