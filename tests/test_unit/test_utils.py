import pytest
#测试hash逻辑
from src.posts.utils import get_password_hash, verify_password

def test_get_password_hash():
    password = "mysupersecretpassword123"
    hashed = get_password_hash(password)

    assert hashed != password
    assert isinstance(hashed, str)

    #测试验证
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False