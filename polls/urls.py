from django.conf.urls import url
from polls import views


urlpatterns = [
    url(r'^$', views.upload, name='uplink'),
    url(r'^download/(.*)', views.download, name="download"),
    url(r'^download_attachment/(.*)/(.*)', views.download_as_attachment,
        name="download_attachment"),
    url(r'^exchange/(.*)', views.exchange, name="exchange"),
    url(r'^parse/(.*)', views.parse, name="parse"),
    url(r'^import/', views.import_data, name="import"),
    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    url(r'^export/(.*)', views.export_data, name="export"),
    url(r'^handson_view/', views.handson_table, name="handson_view"),

    # handson table view
    url(r'^embedded_handson_view/',
        views.embed_handson_table, name="embed_handson_view"),
    url(r'^embedded_handson_view_single/',
        views.embed_handson_table_from_a_single_table,
        name="embed_handson_view"),
    # survey_result
    url('^survey_result/',
        views.survey_result, name='survey_result'),

    # testing purpose
    url(r'^import_using_isave/',
        views.import_data_using_isave_book_as),
    url(r'^import_sheet_using_isave/',
        views.import_sheet_using_isave_to_database),
    url(r'^import_without_bulk_save/',
        views.import_without_bulk_save, name="import_no_bulk_save")
]
