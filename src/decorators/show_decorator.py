try:
    from flask import jsonify
    from functools import wraps
    from models.show import Show
except ImportError:
    print("Error has occurred with imports"
          "Please check importing from modules is correct")


# Show decorator queries show objects within database
# takes keyword argument show_id
# returns kwargs["show"] = show as the band object being passed
def get_show_fromdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            show_id = int(kwargs.get("show_id"))
            show = Show.query\
                .filter_by(id=show_id)\
                    .first_or_404(description=\
                                  "Sorry this show does not exist, \
                                    please check id")

            kwargs["show"] = show

            return func(*args, **kwargs)
        except TypeError:
            return jsonify({"message" : \
                            "Please ensure you input a string"}), 500
        except ValueError:
            return jsonify({"message" : \
                            "Please ensure you input a number"}), 500
    return wrapper