from datetime import date


# -----------------------------------------------------------------------------
# 1.1. Raw strings with r" "
print(r"C:\some\name")  # good
print("C:\some\name")  # bad

# -----------------------------------------------------------------------------
# 1.2. Formatting with repeated ocurrencies
print(
    """
    Hello {name},
    Welcome to {company}. Your new email is: {name}@{company}.
    Regards,

    {date:%Y-%m-%d}
    """.format(
        name="john", company="awesomecompany", date=date.today()
    )
)

# -----------------------------------------------------------------------------
# 1.3. Formatting with f" " (Python 3.6+)

# This will probably change in a for loop or something similar
path = "src/data"
mdate = date(2019, 2, 16)

print(f"{path}/{mdate:%Y-%m-%d}.xlsx")  # Good
print(path + "/" + mdate.strftime("%Y-%m-%d") + ".xlsx")  # Not that good
print("{}/{:%Y-%m-%d}.xlsx".format(path, mdate))  # Old python
