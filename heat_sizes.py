def generate_heat_sizes(num_pilots, max_heat_size=5):
    """
    Generate heat sizes using custom distribution rules:
    - Prefer heats of 5
    - Use heats of 4 or 3 to avoid small leftover groups
    """

    if max_heat_size != 5:
        raise ValueError("This function currently supports max heat size of 5 only")
    
    if num_pilots <= 5:
        return [num_pilots]

    r = num_pilots % 5

    # If number of pilots is already multiple of 5, it's the next multiple
    if r == 0: 
        next_5_multiple = num_pilots
    # If it's no multiple of 5, get the next multiple of 5
    else:
        next_5_multiple = num_pilots + (5 - r)

    # Get how many groups of 5 would have the next multiple
    groups_of_5_for_next_5_multiple = next_5_multiple // 5

    # Get how many groups of each we will need for this case
    five = 0
    four = 0
    three = 0

    # Multiple of 5
    if r == 0:
        five = num_pilots // 5

    # Multiple of 5 - 1
    elif r == 4:
        five = groups_of_5_for_next_5_multiple - 1
        four = 1

    # Multiple of 5 - 2
    elif r == 3:
        five = groups_of_5_for_next_5_multiple - 2
        four = 2

    # Multiple of 5 - 3
    elif r == 2:
        five = groups_of_5_for_next_5_multiple - 2
        four = 1
        three = 1

    # Multiple of 5 - 4
    elif r == 1:
        five = groups_of_5_for_next_5_multiple - 2
        three = 2

    heat_sizes = (
        [3] * max(three, 0) +
        [4] * max(four, 0) +
        [5] * max(five, 0)
    )

    return heat_sizes