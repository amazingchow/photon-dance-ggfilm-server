import random


class PrimaryReplicaRouter:
    """
    A router to control all database operations on models in the
    wechat_ggfilm_backend application.
    """

    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        return random.choice([
                'massive_dev_chart_replica_1',
                'massive_dev_chart_replica_2',
                'massive_dev_chart_replica_3',
            ])

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'massive_dev_chart_primary'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {
            'massive_dev_chart_primary',
            'massive_dev_chart_replica_1',
            'massive_dev_chart_replica_2',
            'massive_dev_chart_replica_3',
        }
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True
