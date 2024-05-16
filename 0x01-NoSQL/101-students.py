"""
this Python function that returns all 
students sorted by average score
"""
def top_students(mongo_collection):
    """
    this function print the average student score
    """
    return mongo_collection.average({}).averageScore