database = r"Test"

# Five standard basketball positions, stored in a list
pos = ["PG", "SG", "SF", "PF", "C"]

# The minimum and maximum rating for skills
min_rating = 10
max_rating = 99

# The average height and standard deviation in cm
# Player heights will be determined with a normal distribution
avg_height = 196.5
height_sd = 8
avg_weight = 24.9*((avg_height/100)**2)

# Define what the skills and tendencies are
skills = ["3pt", "mid", "fin", "dunk",  "ft", "post", "pass", "drive", "dribble", "per_d", "post_d", "blk", "speed",
          "jump", "strength", "oreb", "dreb"]
tendencies = ["3pt", "mid", "pass", "drive", "post", "layup", "dunk", "foul", "stl", "blk"]