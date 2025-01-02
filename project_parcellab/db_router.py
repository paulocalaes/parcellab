# db_router.py
class DatabaseRouter:
    """
    A router to control all database operations on models.
    It directs read queries to the replica database and write queries to the primary database.
    """

    def db_for_read(self, model, **hints):
        """Point all read operations to 'replica'."""
        return 'replica'

    def db_for_write(self, model, **hints):
        """Point all write operations to 'default'."""
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if both models are in the same database."""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that migrations only occur on the default database."""
        return db == 'default'
