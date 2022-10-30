"""Pipeline for social_core.pipelines.user"""
USER_FIELDS = ['email']

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """Create social user function"""
    if user:
        return {'is_new': False}

    fields = {"email_address": kwargs.get(name, details.get(name))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS)}
    if not fields:
        return
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }
