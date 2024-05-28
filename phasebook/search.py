from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!
    search_results = []

    # Check if no search parameters are provided
    if not args:  # If args is empty
        return USERS  # Return all users from the database

    # Check if 'id' parameter is provided
    if 'id' in args:
        user_id = args['id']
        # Find user by ID and include it in the search results
        user = next((user for user in USERS if user['id'] == user_id), None)
        if user:
            search_results.append(user)

    # Iterate over each user in the database
    for user in USERS:
        # Check other search parameters
        if 'name' in args and args['name'].lower() in user['name'].lower():
            search_results.append(user)
        elif 'age' in args:
            try:
                age = int(args['age'])
                user_age = user.get('age', None)
                if user_age is not None and (age - 1 <= user_age <= age + 1):
                    search_results.append(user)
            except ValueError:
                pass  # Ignore non-integer age values
        elif 'occupation' in args:
            search_occupation = args['occupation'].lower()
            user_occupation = user['occupation'].lower()
            if search_occupation in user_occupation or search_occupation == user_occupation:
                search_results.append(user)
                
    # Remove duplicates
    search_results = list({user['id']: user for user in search_results}.values())
    search_results.sort(key=lambda x: x['id'])

    return search_results
