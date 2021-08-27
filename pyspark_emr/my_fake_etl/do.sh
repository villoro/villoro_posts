# First create a package and install it (avoid cache to make sure we pick changes) 
printf "\nPREPARING PACKAGE:\n"
poetry build
printf "\nINSTALLING PACKAGE:\n"
pip install --ignore-installed dist/my_fake_etl-0.1.0-py3-none-any.whl 

# Test the sum
printf "\nTESTING SUM:\n"
python starters/starter_sum.py 2

# Test the greeting
printf "\nTESTING GREETING:\n"
python starters/starter_greet.py hello world

# Test the generic entrypoint for both
printf "\nTESTING GENERIC ENTRY POINT:\n"
python starters/starter_generic.py my_fake_etl.multiply.multiply_2 5
python starters/starter_generic.py my_fake_etl.multiply.multiply_3 5