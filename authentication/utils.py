import jwt


def get_user_id_from_token(request):
    try:
        authorization_header = request.headers.get("Authorization")
        if not authorization_header:
            raise Exception("Authorization header not found")

        token = authorization_header.split()[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        user_id = decoded_token.get("username")
        if not user_id:
            raise Exception("User ID not found in token")
        return user_id
    except jwt.DecodeError:
        raise Exception("Invalid token")
    except jwt.ExpiredSignatureError:
        raise Exception("Expired token")
    except Exception as e:
        raise Exception(f"Error decoding token: {e}")
