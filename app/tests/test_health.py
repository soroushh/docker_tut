"""."""
from app.models.user import User


def test_user_can_be_instantiated_and_gets_proper_attributes():
    """."""
    user_1 = User(
        user_id=1,
        username='soroush',
        email='s@s.com',
        image_file='default.jpg'
    )

    assert isinstance(user_1, User)

    assert user_1.username == 'soroush'
    assert user_1.email == 's@s.com'
    assert user_1.image_file == 'default.jpg'
