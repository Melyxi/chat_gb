from setuptools import find_packages, setup

install_requires = ["asttokens>=2.0,<3.0",
                    "click>=7.0, <7.2",
                    "colorama>=0.0,<0.5.1",
                    "executing>=0.5.0,<0.7.0",
                    "icecream>=1.0, < 3.0",
                    "Pygments>1.9.0,<3.0",
                    "PyQt5>=5.0,<6.0",
                    "PyQt5-Qt5>=5.0,<6.0",
                    "PyQt5-sip>12.0, <13.0",
                    "six>=1.0,<2.0"]

setup(name="project_chat",
      version="1.0",
      description="Chat",
      author="Igor Kuzmin",
      author_email="igorkuz2018@yandex.ru",
      install_requires=install_requires,
      packages=find_packages(),
      entry_points={
          "console_script": [
              "start_client=project_chat.client:main",
              "start_server=project_chat.server:main",
          ]
      }
      )
