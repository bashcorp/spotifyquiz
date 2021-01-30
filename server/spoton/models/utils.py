"""Miscellaneous models used by the Spotify quiz models."""

from django.db import models
from polymorphic.models import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet


class CleanOnSaveMixin:
    """A mixin to for Model classes that cleans models before saving.

    A mixin for any Django Model class or subclass that cleans the
    models before saving them, so that when models are saved, their
    fields are validated.
    """
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)



class PolyOwnerQuerySet(models.QuerySet):
    """Overrides Django QuerySet for a custom deletion method

    Overrides Django's QuerySet class so that deleting a QuerySet
    (a set of database objects) will delete each one individually.
    This is done so that an overridden delete() method in any model
    using this QuerySet will be called. Normally, deleting a QuerySet
    uses SQL commands and ignores the delete() methods.

    Django-Polymorphic has issues deleting sets of PolymorphicModel
    objects, and the fix to this is to override the delete() method of
    any model that contains a set (in a reverse Foreign Key
    relationship) of PolymorphicModel objects. When deleting sets
    of this model, you need to ensure that the overridden method
    is called, which is what this class does.

    For example, let's say ModelA is a PolymorphicModel, with a
    Foreign Key to ModelB, a normal Django model. So ModelB "has" many
    ModelA objects. Django-Polymorphic's issue is with deleting all of
    ModelB's ModelA objects. You need to override the ModelB delete()
    methods so that each ModelA object is deleted individually.
    What about deleting several ModelB objects at once? That won't call
    the overridden delete() method, so make the ModelB class use this
    class as its QuerySet, which will ensure that the overridden
    delete() method in ModelB is called any time a set of ModelB 
    objects is deleted.

    Any Model containing a reverse Foreign Key relationship to a
    PolymorphicModel should override its own delete() method and
    use this class (or the similar PolyOwnerPolymorphicQuerySet)
    as its QuerySet by putting
        objects = PolyOwnerQuerySet.as_manager()
    in its attributes.
    """

    def delete(self, *args, **kwargs):
        """
        Deletes each object in the QuerySet individually, so that the
        set's model's delete() method is called. See above for reasons.
        """
        for obj in self:
            obj.delete()

        super(PolyOwnerQuerySet, self).delete(*args, **kwargs)


class PolyOwnerPolymorphicQuerySet(PolymorphicQuerySet):
    """Overrides PolymorphicQuerySet for a custom deletion method

    Overrides Django-Polymorphic's PolymorphicQuerySet class so that
    deleting a QuerySet (a set of database objects) will delete each
    one individually. This is done so that an overridden delete()
    method in any model using this QuerySet will be called. Normally,
    deleting a QuerySet uses SQL commands and ignores the delete()
    methods.

    Any PolymorphicModel containing a reverse Foreign Key relationship
    to another PolymorphicModel should override its own delete() method
    and use this class as its QuerySet by putting
        objects = PolyOwnerQuerySet.as_manager()
    in its attributes.

    See the PolyOwnerQuerySet documentation for more details on why
    this is needed.
    """

    def delete(self, *args, **kwargs):
        """Deletes each object in the QuerySet individually.

        Deletes each object in the QuerySet individually, so that the
        set's model's delete() method is called. See above for reasons.
        """
        for obj in self:
            obj.delete()

        super(PolyOwnerPolymorphicQuerySet, self).delete(*args, **kwargs)





