# Export the poetry.lock to a requirements.txt
printf "\nEXPORTING requirements.txt\n"
poetry export -f requirements.txt --output requirements.txt

# Prepare a folder for the dependencies
printf "\nCLEANING PREVIOUS EXPORT\n"
[ -e dependencies ] && rm -r dependencies
mkdir dependencies
cd dependencies

# Export dependencies
printf "\nEXPORTING WHEELS:\n"
pip wheel -r ../requirements.txt