from setuptools import setup, find_packages

setup(
  name='aries_cloudagent_webhook_relay',
  version='1.0',
  description='Collects and cache\'s aca-py webhook calls until requested by controller',
  author='Karim Stekelenburg',
  maintainer='Karim Stekelenbrug',
  author_email='karim.stekelenburg@me.com',
  maintainer_email='karim.stekelenburg@me.com',
  install_requires=[
    'aiohttp',
  ],
  package_dir={
    'webhook_relay': 'webhook_relay',
    'webhook_relay.lib': 'webhook_relay/lib'
  },
  packages=['webhook_relay', 'webhook_relay.lib'],
  entry_points={
    'console_scripts': ['webhook-relay=webhook_relay.main:main']
  }
)