import os

#Change the host to adress of the machine which the mongo is hosted
os.environ['MONGO_HOST'] = 'localhost'

# Authentication settings
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Biological data
SIGNIFICANT_VARIANTS = ["S:N501Y","S:N501T", "S:N501S", "S:E484K", "S:K417T", "S:F157L", "S:V367F", "S:Q613H", "S:P681R", "S:Q677H", "S:F888L", "S:H69_V70del", "S:N439K", "S:Y453F", "S:S98F", "S:L452R", "S:D80Y", "S:A626S", "S:V1122L", "S:A222V", "S:S477N"]