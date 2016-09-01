
from flaskr import db



def managed_session():
    """
    トランザクション制御
    :return:
    """

    def _managed_session(func):
        import functools

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                db.session.commit()
                return result
            except Exception as ex:
                current_app.logger.error(ex)
                db.session.rollback()
                raise
            finally:
                db.session.close()

        return wrapper

    return _managed_session
