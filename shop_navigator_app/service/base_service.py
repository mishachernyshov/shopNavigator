"""
Provides tools to work with data models using ORM.
"""


class BaseService:
    """
    Provides methods for executing CRUD operation in the
    database and retrieving information from it.
    """

    def __init__(self, model):
        self.model = model

    def get_all_instances(self, session):
        """
        "SELECT * " analogue
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :return: all the model instances rows
        """
        return session.query(self.model).all()

    def get_first_instance_by_id(self, session, instance_id=None):
        """
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param instance_id: resource identificator to get a specific instance
        :return: an instance row that contains the specified identificator
        """
        return session.query(self.model) \
            .filter_by(id=instance_id).first()

    def get_all_instances_by_id(self, session, instance_id=None):
        """
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param instance_id: resource identificator to get a specific instance
        :return: all the instance rows that contain the specified identificator
        """
        return session.query(self.model) \
            .filter_by(id=instance_id)

    @staticmethod
    def insert_new_instance(session, new_instance):
        """
        Inserts a new model instance into database.
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param new_instance: new model instance to insert
        """
        session.add(new_instance)
        session.commit()

    @staticmethod
    def update_instance(session, model_instance, updated_data):
        """
        Updates a model instance using passed data.
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param model_instance: data instance that should be updated
        :param updated_data: new data that should replace the old one
        """
        model_instance.update(updated_data)
        session.commit()

    @staticmethod
    def delete_instance(session, model_instance):
        """
        Deletes the passed model instance from the database.
        :param session: establishes all conversations with the database
                        and represents a “holding zone” for all the
                        objects which you’ve loaded or associated with
                        it during its lifespan
        :param model_instance: the model instance that must be deleted
        """
        session.delete(model_instance)
        session.commit()
