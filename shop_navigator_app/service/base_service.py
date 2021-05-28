class BaseService:
    def __init__(self, model):
        self.model = model

    def get_all_instances(self, session):
        return session.query(self.model).all()

    def get_first_instance_by_id(self, session, id=None):
        return session.query(self.model) \
            .filter_by(id=id).first()

    def get_all_instances_by_id(self, session, id=None):
        return session.query(self.model) \
            .filter_by(id=id)

    @staticmethod
    def insert_new_instance(session, new_instance):
        session.add(new_instance)
        session.commit()

    @staticmethod
    def update_instance(session, model_instance, updated_data):
        model_instance.update(updated_data)
        session.commit()

    @staticmethod
    def delete_instance(session, model_instance):
        session.delete(model_instance)
        session.commit()
