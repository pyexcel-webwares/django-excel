from django.urls import re_path
from polls import views

urlpatterns = [
    re_path(r'^$', views.upload, name='uplink'),
    re_path(r'^download/(.*)', views.download, name="download"),
    re_path(r'^download_attachment/(.*)/(.*)', views.download_as_attachment,
            name="download_attachment"),
    re_path(r'^exchange/(.*)', views.exchange, name="exchange"),
    re_path(r'^parse/(.*)', views.parse, name="parse"),
    re_path(r'^import/', views.import_data, name="import"),
    re_path(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    re_path(r'^export/(.*)', views.export_data, name="export"),
    re_path(r'^handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    re_path(r'^embedded_handson_view/',
            views.embed_handson_table, name="embed_handson_view"),
    re_path(r'^embedded_handson_view_single/',
            views.embed_handson_table_from_a_single_table,
            name="embed_handson_view"),
    # survey_result
    re_path('^survey_result/',
            views.survey_result, name='survey_result'),

    # testing purpose
    re_path(r'^import_using_isave/',
            views.import_data_using_isave_book_as),
    re_path(r'^import_sheet_using_isave/',
            views.import_sheet_using_isave_to_database),
    re_path(r'^import_without_bulk_save/',
            views.import_without_bulk_save, name="import_no_bulk_save")
]
