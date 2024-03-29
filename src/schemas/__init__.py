try:
    from .user_schema import UserSchema
    from .band_schema import BandSchema
    from .venue_schema import venue_schema
    from .show_schema import ShowSchema
    from .attending_schema import AttendingSchema
    from .playing_schema import PlayingSchema
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")