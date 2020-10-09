# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


class FilmRecordAdmin(admin.ModelAdmin):
    list_display = (
        "film", "developer", "dilution", "asa_iso", "create_timestamp", "update_timestamp",
    )

    list_filter = (
        "film",
    )


class MassiveDevChartFilmAdmin(admin.ModelAdmin):
    list_display = (
        "name", "create_timestamp", "update_timestamp",
    )

    list_filter = (
        "name",
    )


class MassiveDevChartDeveloperAdmin(admin.ModelAdmin):
    list_display = (
        "name", "create_timestamp", "update_timestamp",
    )

    list_filter = (
        "name",
    )


class MassiveDevChartNoteAdmin(admin.ModelAdmin):
    list_display = (
        "note", "remark", "create_timestamp", "update_timestamp",
    )

    list_filter = (
        "note",
    )


admin.site.register(models.FilmRecord, FilmRecordAdmin)
admin.site.register(models.MassiveDevChartFilm, MassiveDevChartFilmAdmin)
admin.site.register(models.MassiveDevChartDeveloper, MassiveDevChartDeveloperAdmin)
admin.site.register(models.MassiveDevChartNote, MassiveDevChartNoteAdmin)
