try:
    from controllers.user_controller import users
    from controllers.band_controller import bands
    from controllers.venue_controller import venues
    from controllers.show_controller import shows
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")

registerable_controllers = [
    users,
    bands,
    venues,
    shows
]