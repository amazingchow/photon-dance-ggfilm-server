# -*- coding: utf-8 -*-
from django.db import models


class FilmRecord(models.Model):
    film        = models.CharField(max_length=127, db_index=True)
    developer   = models.CharField(max_length=127)
    dilution    = models.CharField(max_length=127)
    asa_iso     = models.CharField(max_length=127)
    a35mm       = models.CharField(max_length=127)
    a120        = models.CharField(max_length=127)
    sheet       = models.CharField(max_length=127)
    temp        = models.CharField(max_length=127)
    notes       = models.CharField(max_length=127)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.film

    def __str__(self):
        return "(film-record: \
            (\t\nfilm: {}\t\ndeveloper: {}\t\ndilution: {}\t\niso: {}\t\n35mm: {}\t\n120: {}\t\nsheet: {}\t\ntemp: {}\t\nnotes: {}\t\n))"\
                .format(self.film)

    class Meta:
        verbose_name = "The Massive Dev Chart - Film Record"
        verbose_name_plural = "The Massive Dev Chart - Film Record"


class FilmRecordUpdateLocker(models.Model):
    name = models.CharField(verbose_name="locker's name", max_length=31)
    the_first = models.BooleanField(verbose_name="is the first time to create or not", default=False)
    update = models.IntegerField(verbose_name="how many times we have updated the records", default=0)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "({}: {})".format(self.name, self.update)

    class Meta:
        verbose_name = "The Massive Dev Chart - Film Record Update Locker"
        verbose_name_plural = "The Massive Dev Chart - Film Record Update Locker"


class MassiveDevChartFilm(models.Model):
    name = models.CharField(max_length=127)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "(film: {})".format(self.name)

    class Meta:
        verbose_name = "The Massive Dev Chart - Film"
        verbose_name_plural = "The Massive Dev Chart - Film"


class MassiveDevChartDeveloper(models.Model):
    name = models.CharField(max_length=127)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return "(developer: {})".format(self.name)

    class Meta:
        verbose_name = "The Massive Dev Chart - Developer"
        verbose_name_plural = "The Massive Dev Chart - Developer"


class MassiveDevChartNote(models.Model):
    note   = models.CharField(max_length=127)
    remark = models.CharField(max_length=255)

    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.note

    def __str__(self):
        return "(note: {})".format(self.note)

    class Meta:
        verbose_name = "The Massive Dev Chart - Note"
        verbose_name_plural = "The Massive Dev Chart - Note"
