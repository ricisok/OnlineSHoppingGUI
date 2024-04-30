from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        # 这是一个设置方法，在每个测试方法运行前执行。
        self.username = "newuser"
        self.email = "newuser@example.com"
        self.password = "securepassword123"

    def test_user_registration(self):
        # 测试用户注册功能
        response = self.client.post(reverse('register'), {
            'username': self.username,
            'email': self.email,
            'password1': self.password,  # 假设使用了两次密码确认
            'password2': self.password
        })

        # 检查是否重定向到正确的页面（例如主页）
        self.assertRedirects(response, reverse('home'))

        # 检查用户是否在数据库中
        user = User.objects.get(username=self.username)
        self.assertIsNotNone(user)

        # 检查用户的邮箱是否设置正确
        self.assertEqual(user.email, self.email)

        # 最后，检查密码是否正确
        self.assertTrue(user.check_password(self.password))

# 运行测试
if __name__ == '__main__':
    unittest.main()
