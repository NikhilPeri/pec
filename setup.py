from distutils.core import setup

setup(
    name = 'pec',
    packages = ['pec'],
    version = '1.0.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'Priorty Expire Cache',
    author = 'Nik Peri',
    author_email = 'nperi@tesla.com',
    url = 'https://github.com/NikhilPeri/pec',
    download_url = 'https://github.com/NikhilPeri/pec.git',
    install_requires=['blist==1.3.6']
)
